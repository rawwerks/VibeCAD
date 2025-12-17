#!/usr/bin/env python3
"""
3D Model Diff - Compare two CAD models using boolean operations.

Usage:
    uvx --from build123d python model_diff.py <reference> <generated>
    uvx --from build123d python model_diff.py gold.step predicted.step --json
    uvx --from build123d python model_diff.py --demo

Supported formats: STEP (.step, .stp), BREP (.brep), STL (.stl)

Computes:
    - IoU (Intersection over Union) - primary similarity metric
    - Dice coefficient (F1 score for volumes)
    - Precision (how much of generated is correct)
    - Recall (how much of reference was captured)
    - Spatial metrics (center offset, bounding box, size ratios)

Outputs:
    - Human-readable comparison report
    - JSON metrics for training pipelines
    - GLB visualization files (optional)
"""
import argparse
import json
import sys
from pathlib import Path

from build123d import (
    Box, Cylinder, Sphere, Pos,
    export_gltf, export_step,
    import_step, import_brep, import_stl
)


# =============================================================================
# Model Loading
# =============================================================================

SUPPORTED_FORMATS = {'.step', '.stp', '.brep', '.stl'}


def load_model(filepath):
    """
    Load a 3D model from file.

    Supported formats:
        - STEP (.step, .stp) - recommended for CAD models
        - BREP (.brep) - OpenCASCADE native format
        - STL (.stl) - mesh format (limited boolean support)

    Args:
        filepath: Path to the model file

    Returns:
        build123d shape object
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Model file not found: {filepath}")

    suffix = path.suffix.lower()

    if suffix in ('.step', '.stp'):
        return import_step(str(path))
    elif suffix == '.brep':
        return import_brep(str(path))
    elif suffix == '.stl':
        return import_stl(str(path))
    else:
        raise ValueError(
            f"Unsupported format: {suffix}\n"
            f"Supported: {', '.join(sorted(SUPPORTED_FORMATS))}"
        )


# =============================================================================
# Boolean Diff Operations
# =============================================================================

def diff_models(reference, generated):
    """
    Compute boolean difference between two models.

    Args:
        reference: The gold/target model (A)
        generated: The predicted/test model (B)

    Returns:
        tuple: (missing, extra, common)
            - missing: geometry in reference but not in generated (A - B)
            - extra: geometry in generated but not in reference (B - A)
            - common: geometry shared by both (A & B)
    """
    missing = reference - generated  # What's in A but not B
    extra = generated - reference    # What's in B but not A
    common = reference & generated   # What's in both

    return missing, extra, common


# =============================================================================
# Metrics Computation
# =============================================================================

def compute_metrics(reference, generated, common):
    """
    Compute comprehensive comparison metrics.

    Args:
        reference: The gold/target model (A)
        generated: The predicted/test model (B)
        common: The intersection (A & B)

    Returns:
        dict: All computed metrics
    """
    vol_ref = reference.volume
    vol_gen = generated.volume
    vol_common = common.volume
    vol_union = vol_ref + vol_gen - vol_common

    metrics = {}

    # === Primary Metrics (for training/evaluation) ===

    # IoU (Jaccard Index): standard similarity metric
    # Range: 0 (no overlap) to 1 (identical)
    metrics["iou"] = vol_common / vol_union if vol_union > 0 else 1.0

    # Dice coefficient (F1 score for volumes)
    # More sensitive than IoU for small overlaps
    # Dice = 2 * |A ∩ B| / (|A| + |B|)
    denom = vol_ref + vol_gen
    metrics["dice"] = 2 * vol_common / denom if denom > 0 else 1.0

    # Precision: How much of generated is correct?
    # High precision = not much extra/wrong geometry
    metrics["precision"] = vol_common / vol_gen if vol_gen > 0 else 0.0

    # Recall: How much of reference did we capture?
    # High recall = captured most of the target
    metrics["recall"] = vol_common / vol_ref if vol_ref > 0 else 0.0

    # F1 from precision/recall (should match dice)
    p, r = metrics["precision"], metrics["recall"]
    metrics["f1"] = 2 * p * r / (p + r) if (p + r) > 0 else 0.0

    # === Volume Metrics ===

    metrics["volume_reference"] = vol_ref
    metrics["volume_generated"] = vol_gen
    metrics["volume_intersection"] = vol_common
    metrics["volume_union"] = vol_union
    metrics["volume_ratio"] = vol_gen / vol_ref if vol_ref > 0 else 0.0

    # === Spatial Metrics ===

    # Center of mass offset
    try:
        center_ref = reference.center()
        center_gen = generated.center()
        offset = (
            (center_gen.X - center_ref.X) ** 2 +
            (center_gen.Y - center_ref.Y) ** 2 +
            (center_gen.Z - center_ref.Z) ** 2
        ) ** 0.5
        metrics["center_offset"] = offset
        metrics["center_reference"] = (center_ref.X, center_ref.Y, center_ref.Z)
        metrics["center_generated"] = (center_gen.X, center_gen.Y, center_gen.Z)
    except Exception:
        metrics["center_offset"] = None

    # Bounding box comparison
    try:
        bb_ref = reference.bounding_box()
        bb_gen = generated.bounding_box()

        size_ref = (
            bb_ref.max.X - bb_ref.min.X,
            bb_ref.max.Y - bb_ref.min.Y,
            bb_ref.max.Z - bb_ref.min.Z
        )
        size_gen = (
            bb_gen.max.X - bb_gen.min.X,
            bb_gen.max.Y - bb_gen.min.Y,
            bb_gen.max.Z - bb_gen.min.Z
        )

        metrics["bbox_size_reference"] = size_ref
        metrics["bbox_size_generated"] = size_gen

        # Size ratios per axis
        metrics["size_ratio_x"] = size_gen[0] / size_ref[0] if size_ref[0] > 0 else 0.0
        metrics["size_ratio_y"] = size_gen[1] / size_ref[1] if size_ref[1] > 0 else 0.0
        metrics["size_ratio_z"] = size_gen[2] / size_ref[2] if size_ref[2] > 0 else 0.0

        # Bounding box IoU
        min_x = max(bb_ref.min.X, bb_gen.min.X)
        min_y = max(bb_ref.min.Y, bb_gen.min.Y)
        min_z = max(bb_ref.min.Z, bb_gen.min.Z)
        max_x = min(bb_ref.max.X, bb_gen.max.X)
        max_y = min(bb_ref.max.Y, bb_gen.max.Y)
        max_z = min(bb_ref.max.Z, bb_gen.max.Z)

        intersection_vol = (
            max(0, max_x - min_x) *
            max(0, max_y - min_y) *
            max(0, max_z - min_z)
        )
        box_vol_ref = size_ref[0] * size_ref[1] * size_ref[2]
        box_vol_gen = size_gen[0] * size_gen[1] * size_gen[2]
        box_union = box_vol_ref + box_vol_gen - intersection_vol

        metrics["bbox_iou"] = intersection_vol / box_union if box_union > 0 else 1.0
    except Exception:
        metrics["bbox_iou"] = None

    # === Surface Metrics ===

    try:
        metrics["surface_reference"] = reference.area
        metrics["surface_generated"] = generated.area
        metrics["surface_ratio"] = generated.area / reference.area if reference.area > 0 else 0.0
    except Exception:
        metrics["surface_ratio"] = None

    # === Topology Metrics ===

    try:
        metrics["faces_reference"] = len(reference.faces())
        metrics["faces_generated"] = len(generated.faces())
        metrics["edges_reference"] = len(reference.edges())
        metrics["edges_generated"] = len(generated.edges())
        metrics["vertices_reference"] = len(reference.vertices())
        metrics["vertices_generated"] = len(generated.vertices())
    except Exception:
        pass

    return metrics


# =============================================================================
# Output Formatting
# =============================================================================

def print_report(reference, generated, missing, extra, common, metrics):
    """Print human-readable comparison report."""

    print("\n" + "=" * 65)
    print("  3D MODEL COMPARISON REPORT")
    print("  Reference (A) vs Generated (B)")
    print("=" * 65)

    # Volumes
    print(f"\n{'─── VOLUMES ───':─^65}")
    print(f"  Reference (A):      {metrics['volume_reference']:>14,.3f}")
    print(f"  Generated (B):      {metrics['volume_generated']:>14,.3f}")
    print(f"  Intersection (A∩B): {metrics['volume_intersection']:>14,.3f}")
    print(f"  Union (A∪B):        {metrics['volume_union']:>14,.3f}")
    print(f"  Missing (A-B):      {missing.volume:>14,.3f}  "
          f"({100 * missing.volume / metrics['volume_reference']:.1f}% of A)")
    print(f"  Extra (B-A):        {extra.volume:>14,.3f}  "
          f"({100 * extra.volume / metrics['volume_generated']:.1f}% of B)")

    # Primary metrics
    print(f"\n{'─── PRIMARY METRICS ───':─^65}")
    print(f"  IoU (Jaccard):      {metrics['iou']:>14.4f}  (1.0 = identical)")
    print(f"  Dice (F1):          {metrics['dice']:>14.4f}  (1.0 = identical)")
    print(f"  Precision:          {metrics['precision']:>14.4f}  (correctness of B)")
    print(f"  Recall:             {metrics['recall']:>14.4f}  (coverage of A)")

    # Diagnostic metrics
    print(f"\n{'─── DIAGNOSTIC METRICS ───':─^65}")
    print(f"  Volume ratio (B/A): {metrics['volume_ratio']:>14.4f}  (1.0 = same size)")

    if metrics.get('surface_ratio'):
        print(f"  Surface ratio:      {metrics['surface_ratio']:>14.4f}")

    if metrics.get('center_offset') is not None:
        print(f"  Center offset:      {metrics['center_offset']:>14.4f} units")

    if metrics.get('bbox_iou') is not None:
        print(f"  BBox IoU:           {metrics['bbox_iou']:>14.4f}")
        print(f"  Size ratio X:       {metrics['size_ratio_x']:>14.4f}")
        print(f"  Size ratio Y:       {metrics['size_ratio_y']:>14.4f}")
        print(f"  Size ratio Z:       {metrics['size_ratio_z']:>14.4f}")

    if metrics.get('faces_reference') is not None:
        print(f"\n{'─── TOPOLOGY ───':─^65}")
        print(f"  Faces:    {metrics['faces_reference']:>6} (A)  vs  {metrics['faces_generated']:>6} (B)")
        print(f"  Edges:    {metrics['edges_reference']:>6} (A)  vs  {metrics['edges_generated']:>6} (B)")
        print(f"  Vertices: {metrics['vertices_reference']:>6} (A)  vs  {metrics['vertices_generated']:>6} (B)")

    # Interpretation
    print(f"\n{'─── INTERPRETATION ───':─^65}")

    if metrics['iou'] > 0.95:
        print("  ✓ Excellent match (IoU > 95%)")
    elif metrics['iou'] > 0.8:
        print("  ○ Good match (IoU > 80%)")
    elif metrics['iou'] > 0.5:
        print("  △ Partial match (IoU > 50%)")
    else:
        print("  ✗ Poor match (IoU < 50%)")

    if metrics['precision'] < metrics['recall'] - 0.05:
        print(f"  → Over-generating: {100 * (1 - metrics['precision']):.1f}% of B is extra geometry")
    elif metrics['recall'] < metrics['precision'] - 0.05:
        print(f"  → Under-generating: {100 * (1 - metrics['recall']):.1f}% of A is missing")

    if metrics['volume_ratio'] < 0.95:
        print(f"  → Undersized by {100 * (1 - metrics['volume_ratio']):.1f}%")
    elif metrics['volume_ratio'] > 1.05:
        print(f"  → Oversized by {100 * (metrics['volume_ratio'] - 1):.1f}%")

    if metrics.get('center_offset', 0) > 1.0:
        print(f"  → Center offset: {metrics['center_offset']:.2f} units from reference")

    print("=" * 65)


def get_json_metrics(metrics):
    """Get JSON-serializable metrics dict."""
    # Filter out None values and non-serializable types
    result = {}
    for k, v in metrics.items():
        if v is None:
            continue
        if isinstance(v, (int, float, str, bool)):
            result[k] = v
        elif isinstance(v, tuple):
            result[k] = list(v)
    return result


# =============================================================================
# Demo Models
# =============================================================================

def create_demo_models():
    """Create demo models for testing the diff tool."""
    # Reference: box with centered cylindrical hole
    reference = Box(40, 40, 40) - Cylinder(radius=10, height=50)

    # Generated: similar but hole is offset and larger
    generated = Box(40, 40, 40) - Pos(5, 5, 0) * Cylinder(radius=12, height=50)

    return reference, generated


# =============================================================================
# Main Entry Point
# =============================================================================

def run_diff(reference, generated, output_dir=None, export_glb=True):
    """
    Run the complete diff analysis.

    Args:
        reference: Reference model
        generated: Generated model to compare
        output_dir: Directory for output files
        export_glb: Whether to export GLB visualization files

    Returns:
        dict: All computed metrics
    """
    output_dir = Path(output_dir) if output_dir else Path(".")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Compute diff
    missing, extra, common = diff_models(reference, generated)

    # Compute metrics
    metrics = compute_metrics(reference, generated, common)

    # Export visualization GLBs
    if export_glb:
        exports = [
            (reference, "diff_reference.glb", "Reference model (A)"),
            (generated, "diff_generated.glb", "Generated model (B)"),
            (missing, "diff_missing.glb", "Missing geometry (A-B)"),
            (extra, "diff_extra.glb", "Extra geometry (B-A)"),
            (common, "diff_common.glb", "Common geometry (A∩B)"),
        ]

        print(f"\nExporting to {output_dir}/:")
        for shape, filename, description in exports:
            path = output_dir / filename
            try:
                export_gltf(shape, str(path), binary=True)
                print(f"  {filename:25} - {description}")
            except Exception as e:
                print(f"  {filename:25} - Failed: {e}", file=sys.stderr)

    return metrics, missing, extra, common


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "reference",
        nargs="?",
        help="Reference/gold model file (STEP, BREP, or STL)"
    )
    parser.add_argument(
        "generated",
        nargs="?",
        help="Generated/predicted model file to compare"
    )
    parser.add_argument(
        "-o", "--output-dir",
        default=".",
        help="Output directory for GLB files (default: current dir)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output only JSON metrics (for pipelines)"
    )
    parser.add_argument(
        "--no-export",
        action="store_true",
        help="Skip exporting GLB visualization files"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run with built-in demo models"
    )

    args = parser.parse_args()

    # Load models
    if args.demo:
        if not args.json:
            print("Running with demo models...", file=sys.stderr)
        reference, generated = create_demo_models()
    elif args.reference and args.generated:
        if not args.json:
            print(f"Loading reference: {args.reference}", file=sys.stderr)
            print(f"Loading generated: {args.generated}", file=sys.stderr)
        reference = load_model(args.reference)
        generated = load_model(args.generated)
    else:
        parser.print_help()
        print("\nError: Provide two model files or use --demo", file=sys.stderr)
        sys.exit(1)

    # Run diff
    metrics, missing, extra, common = run_diff(
        reference,
        generated,
        output_dir=args.output_dir,
        export_glb=not args.no_export and not args.json
    )

    # Output results
    if args.json:
        print(json.dumps(get_json_metrics(metrics)))
    else:
        print_report(reference, generated, missing, extra, common, metrics)
        print("\n" + "=" * 65)
        print("JSON OUTPUT")
        print("=" * 65)
        print(json.dumps(get_json_metrics(metrics), indent=2))


if __name__ == "__main__":
    main()
