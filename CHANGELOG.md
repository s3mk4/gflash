# Changelog

All notable changes to this project will be documented in this file.

## [0.3.2] - 2026-07-10

### Added
- Watch mode for automatic device detection in fastboot
- Auto-flash option to start flashing automatically on device connection
- Perfect for development workflows with frequent flashing iterations
- Interactive selection menu when device is detected
- Device connection/disconnection tracking with live status

### Improved
- Better logging for watch mode operations
- More informative console output

## [0.3.1] - 2026-07-09

### Added
- gflash-config.py - interactive configuration builder
- Create JSON configs via CLI without manual editing
- Configuration preview before saving
- Support for all config fields including SHA256 hashes

### Improved
- Input data validation in configurator
- Better error messages

## [0.3.0] - 2026-07-08

### Added
- Dry-run mode for configuration validation
- Pre-flight checks without device contact
- Detailed report of what will be flashed
- Support for SHA256 verification in dry-run mode
- Information about total data size to transfer

### Improved
- Configuration validation before flashing
- User safety with pre-flight checks

## [0.2.4] - 2026-07-07

### Added
- Backup functionality to save partitions from device
- backup-all command for mass backup from config
- SHA256 verification during backup operations
- Support for SHA256 hashes in config for verification
- Detailed progress bars during backup

### Improved
- Added insurance mechanism before flash-all
- Users can now cache device state before modifications

## [0.2.3] - 2026-07-06

### Added
- Flash-all command for batch flashing from JSON config
- Support for required and optional partitions
- Configurable partition flashing order
- Automatic partition erasing after flashing
- Support for relative paths in configuration files
- Detailed configuration validation

### Improved
- Reduced need for manual partition-by-partition flashing

## [0.2.2] - 2026-07-05

### Added
- Chunked streaming data transfer (4MB chunks)
- Progress bars for file hashing and upload
- Support for files up to 2GB on memory-limited systems
- More informative output with sizes in MB

### Improved
- Reduced RAM usage during flashing
- Better performance on large files
- Enhanced response validation from device

## [0.2.1] - 2026-07-04

### Added
- Complete logging to gflash.log file
- Utility versioning
- Detailed USB error handling
- SHA256 file integrity checks before flashing

### Improved
- Better error tracking and debugging
- Comprehensive operation logging

## [0.2.0] - 2026-07-03

### Added
- Safe partitions list (SAFE_PARTITIONS)
- Critical partitions list (CRITICAL_PARTITIONS)
- Partition name validation to prevent injection attacks
- Mandatory confirmation for dangerous operations
- Protection against accidental device brick

### Improved
- Multi-level safety mechanisms

## [0.1.0] - 2026-07-02

### Initial Release
- Basic fastboot protocol implementation
- USB device detection
- Single partition flashing capability
- Basic error handling
