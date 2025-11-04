#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2025 The Evolution X Project
# SPDX-License-Identifier: Apache-2.0

import argparse
import os
import hashlib
import json

def generate_json(target_device, product_out, file_name, build_variant):
    output = os.path.join(product_out, f"{target_device}.json")

    if os.path.exists(output):
        os.remove(output)

    buildprop = os.path.join(product_out, "system", "build.prop")
    version = get_version_from_buildprop(buildprop)
    filename = file_name
    url = f"https://sourceforge.net/projects/vendor-ota/files/Pixel/X6882/16/{file_name}/download"
    timestamp = get_timestamp_from_buildprop(buildprop)
    id = get_checksum(os.path.join(product_out, file_name))
    size = os.path.getsize(os.path.join(product_out, file_name))

    json_data = {
        "response": [
            {
                "datetime": timestamp,
                "filename": filename,
                "id": id,
                "size": size,
                "url": url,
                "version": version,
            }
        ]
    }

    with open(output, 'w') as f:
        json.dump(json_data, f, indent=2)

def get_timestamp_from_buildprop(buildprop_path):
    with open(buildprop_path, 'r') as f:
        for line in f:
            if "ro.system.build.date.utc" in line:
                return int(line.split('=')[1].strip())
    return 0

def get_version_from_buildprop(buildprop_path):
    with open(buildprop_path, 'r') as f:
        for line in f:
            if line.startswith("ro.build.version.release="):
                return line.split('=')[1].strip()
    return "0"

def get_checksum(file_path):
    return calculate_sha256(file_path)

def calculate_sha256(file_path):
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def main():
    parser = argparse.ArgumentParser(description="Generate a JSON file for OTA.")
    parser.add_argument("target_device", help="Target device name")
    parser.add_argument("product_out", help="Product output directory")
    parser.add_argument("file_name", help="File name for OTA")
    parser.add_argument("build_variant", help="Build variant")

    args = parser.parse_args()
    generate_json(args.target_device, args.product_out, args.file_name, args.build_variant)

if __name__ == "__main__":
    main()
