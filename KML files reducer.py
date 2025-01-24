import os
import xml.etree.ElementTree as ET
cwd = os.getcwd()


def reduce_coordinate_precision(coordinate_str, precision=6, remove_altitude=False):
    """
    Reduce the precision of coordinates in a KML string and optionally remove altitude.
    """
    coordinates = coordinate_str.strip().split()
    optimized = []
    for coord in coordinates:
        parts = coord.split(",")
        if remove_altitude and len(parts) > 2:
            parts = parts[:2]  # Keep only longitude and latitude
        optimized.append(",".join(f"{float(part):.{precision}f}" for part in parts))
    return " ".join(optimized)


def minify_kml(root):
    """
    Minify KML by removing unnecessary whitespace and line breaks.
    """
    for elem in root.iter():
        if elem.text:
            elem.text = elem.text.strip()
        if elem.tail:
            elem.tail = elem.tail.strip()


def remove_unused_tags(root, tags_to_remove):
    """
    Remove specified tags from the KML structure.
    """
    for tag in tags_to_remove:
        for elem in root.findall(f".//{tag}"):
            parent = elem.getparent()
            if parent is not None:
                parent.remove(elem)


def deduplicate_coordinates(coordinate_str):
    """
    Remove consecutive duplicate coordinates from a string.
    """
    coordinates = coordinate_str.strip().split()
    unique_coords = []
    prev_coord = None
    for coord in coordinates:
        if coord != prev_coord:
            unique_coords.append(coord)
            prev_coord = coord
    return " ".join(unique_coords)


def validate_kml(file_path):
    """
    Validate the KML file by attempting to parse it.
    """
    try:
        ET.parse(file_path)
        return True
    except ET.ParseError:
        return False


def get_file_statistics(file_path):
    """
    Get statistics about the KML file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    size = os.path.getsize(file_path)
    coordinate_count = content.count("<coordinates>")
    return size, coordinate_count


def optimize_kml(input_file, output_file, precision=6, remove_altitude=False, deduplicate=False, tags_to_remove=None):
    """
    Optimize a KML file with customizable options.
    """
    # Get initial statistics
    original_size, original_coordinates = get_file_statistics(input_file)

    # Parse the KML
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Reduce precision and optionally remove altitude
    for elem in root.iter():
        if elem.tag.endswith("coordinates") and elem.text:
            optimized_coords = reduce_coordinate_precision(elem.text, precision, remove_altitude)
            if deduplicate:
                optimized_coords = deduplicate_coordinates(optimized_coords)
            elem.text = optimized_coords

    # Remove specified tags if any
    if tags_to_remove:
        remove_unused_tags(root, tags_to_remove)

    # Minify the KML
    minify_kml(root)

    # Write the optimized KML to the output file
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

    # Validate the output file
    is_valid = validate_kml(output_file)

    # Get final statistics
    optimized_size, optimized_coordinates = get_file_statistics(output_file)

    # Print statistics and validation results
    print("\nKML Optimization Summary:")
    print(f"Original File Size: {original_size / 1024:.2f} KB")
    print(f"Optimized File Size: {optimized_size / 1024:.2f} KB")
    print(f"Original Coordinate Count: {original_coordinates}")
    print(f"Optimized Coordinate Count: {optimized_coordinates}")
    print(f"Validation: {'Passed' if is_valid else 'Failed'}")

    if is_valid:
        print(f"Optimized KML saved to: {output_file}")
    else:
        print("Error: The optimized KML file is invalid!")
def file_reducer(filename):

    input_kml = cwd+"/"+filename  # Replace with your input KML file path
    output_kml = cwd+"/"+filename[:-4]+"_output.kml"  # Replace with your desired output file path

    # Customization options
    coordinate_precision = 6  # Decimal precision for coordinates
    remove_alt = True  # Remove altitude from coordinates
    deduplicate_coords = True  # Deduplicate consecutive coordinates
    tags_to_remove = ["description", "Style"]  # Tags to remove

    optimize_kml(
        input_file=input_kml,
        output_file=output_kml,
        precision=coordinate_precision,
        remove_altitude=remove_alt,
        deduplicate=deduplicate_coords,
        tags_to_remove=tags_to_remove,
    )

# Example usage
if __name__ == "__main__":
    filename="20241212_Cangas_new_Fix Bi_GCR40_320kW_615W_6977_middleandnorth.kml"
    file_reducer(filename)