#!/bin/bash
# Script to create the AI-Commit installer for Linux
# Exit on error
set -e

echo "--- Starting Linux build process ---"

# 1. Create & activate virtual environment
echo "--- Setting up Python virtual environment ---"
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
echo "--- Installing dependencies from requirements.txt ---"
pip install -r requirements.txt

# 3. Run PyInstaller
echo "--- Building executable with PyInstaller ---"
pyinstaller --name "AI-Commit" --windowed --onefile --icon="assets/icon.ico" main.py

# 4. Prepare installer package
echo "--- Creating Linux installer package ---"
INSTALLER_DIR="ai-commit-linux-installer"
rm -rf $INSTALLER_DIR
mkdir -p $INSTALLER_DIR/usr/local/bin
mkdir -p $INSTALLER_DIR/usr/share/applications
mkdir -p $INSTALLER_DIR/usr/share/icons/hicolor/256x256/apps

# Copy necessary files
cp dist/AI-Commit $INSTALLER_DIR/usr/local/bin/ai-commit
cp assets/icon.png $INSTALLER_DIR/usr/share/icons/hicolor/256x256/apps/ai-commit.png
cp scripts/ai-commit.desktop $INSTALLER_DIR/usr/share/applications/

# Create the installation script
cat > $INSTALLER_DIR/install.sh <<EOL
#!/bin/bash
echo "Installing AI-Commit..."
sudo cp -r usr /
echo "Updating icon cache..."
sudo gtk-update-icon-cache /usr/share/icons/hicolor || echo "Failed to update icon cache."
echo "Installation complete. Run 'ai-commit' from your terminal or find it in your applications menu."
EOL
chmod +x $INSTALLER_DIR/install.sh

# Create the tar.gz archive
TARBALL_NAME="AI-Commit-Linux-Installer.tar.gz"
echo "--- Packaging installer into $TARBALL_NAME ---"
tar -czvf $TARBALL_NAME -C $INSTALLER_DIR .

echo "--- Build complete! ---"
echo "Installer created: $TARBALL_NAME"
echo "To install, extract the archive and run './install.sh'"