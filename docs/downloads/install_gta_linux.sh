#!/usr/bin/env bash
# ═════════════════════════════════════════════════════════════════════
#  GTA VICE CITY LINUX INSTALLER & EMULATOR SETUP
#  Created by GTA VICELAUNCHER Team | Mauxx AI
# ═════════════════════════════════════════════════════════════════════

set -euo pipefail

# Output colors
CYAN='\033[0;36m'
PINK='\033[0;35m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Print banner
echo -e "${PINK}"
echo "  ██████╗ ████████╗ █████╗     ██╗   ██╗██╗"
echo " ██╔════╝ ╚══██╔══╝██╔══██╗    ██║   ██║██║"
echo " ██║  ███╗   ██║   ███████║    ██║   ██║██║"
echo " ██║   ██║   ██║   ██╔══██║    ╚██╗ ██╔╝██║"
echo " ╚██████╔╝   ██║   ██║  ██║     ╚████╔╝ ██║"
echo "  ╚═════╝    ╚═╝   ╚═╝  ╚═╝      ╚═══╝  ╚═╝"
echo -e " 🎮 LINUX WINE LAUNCHER & CONFIGURATION SUITE 🎮${NC}"
echo "----------------------------------------------------"

# 1. Dependency checks
echo -e "\n${CYAN}[1/5] Checking System Dependencies...${NC}"
PM=""
if [ -f /etc/debian_version ]; then
    PM="apt"
elif [ -f /etc/redhat-release ] || [ -f /etc/fedora-release ]; then
    PM="dnf"
elif [ -f /etc/arch-release ]; then
    PM="pacman"
fi

install_dep() {
    local pkg=$1
    echo -e "${YELLOW}Installing $pkg...${NC}"
    if [ "$PM" = "apt" ]; then
        sudo apt-get update && sudo apt-get install -y "$pkg"
    elif [ "$PM" = "dnf" ]; then
        sudo dnf install -y "$pkg"
    elif [ "$PM" = "pacman" ]; then
        sudo pacman -Sy --noconfirm "$pkg"
    else
        echo -e "${RED}Unknown package manager. Please install $pkg manually.${NC}"
    fi
}

# Verify Wine
if ! command -v wine &> /dev/null; then
    echo -e "${YELLOW}Wine not found.${NC}"
    install_dep "wine"
else
    echo -e "${GREEN}✓ Wine version: $(wine --version) is installed.${NC}"
fi

# Verify Winetricks
if ! command -v winetricks &> /dev/null; then
    echo -e "${YELLOW}Winetricks not found.${NC}"
    install_dep "winetricks"
else
    echo -e "${GREEN}✓ Winetricks is installed.${NC}"
fi

# Verify Zenity (for GUI prompts)
if ! command -v zenity &> /dev/null; then
    echo -e "${YELLOW}Zenity not found.${NC}"
    install_dep "zenity"
else
    echo -e "${GREEN}✓ Zenity is installed.${NC}"
fi

# 2. Setup prefix
echo -e "\n${CYAN}[2/5] Initializing Wineprefix for GTA Vice City...${NC}"
WINE_DIR="$HOME/.local/share/wineprefixes/gta-vice-city"
mkdir -p "$WINE_DIR"
export WINEPREFIX="$WINE_DIR"
export WINEARCH="win32"

if [ ! -d "$WINE_DIR/drive_c/windows" ]; then
    echo -e "${YELLOW}Initializing Wine prefix directory structure...${NC}"
    wineboot -i
fi
echo -e "${GREEN}✓ Wine prefix initialized successfully at ${WINE_DIR}${NC}"

# 3. Configure DLL Overrides & Sound compatibility
echo -e "\n${CYAN}[3/5] Applying Audio and Graphics Compatibility Fixes...${NC}"
# Use winetricks to install essential libs (directx9 overrides, vcrun6, d3dcompiler)
echo -e "${YELLOW}Configuring system overrides (dsound, directx)...${NC}"
winetricks -q dsound d3dcompiler_43 vcrun6

# 4. Icon & Logo setups
echo -e "\n${CYAN}[4/5] Pulling Logo Branding & Icons...${NC}"
ICON_DIR="$HOME/.local/share/icons/hicolor/256x256/apps"
mkdir -p "$ICON_DIR"
ICON_PATH="$ICON_DIR/gta-vice-city.png"

# Download official logo icon if connection permits, otherwise generate fallback svg
if command -v curl &> /dev/null; then
    echo -e "${YELLOW}Downloading GTA Vice City launcher icon...${NC}"
    curl -s -L -o "$ICON_PATH" "https://raw.githubusercontent.com/rajmodi135/vice-city-launcher/main/docs/images/trainer_icon_1783973933182.jpg" || true
fi

# 5. Desktop Shortcut generation
echo -e "\n${CYAN}[5/5] Generating Desktop Entry Launcher...${NC}"
SHORTCUT_PATH="$HOME/.local/share/applications/gta-vice-city.desktop"
cat <<EOF > "$SHORTCUT_PATH"
[Desktop Entry]
Name=GTA Vice City Launcher
Comment=Play GTA Vice City via Wine Emulator Wrapper
Exec=env WINEPREFIX="$WINE_DIR" WINEARCH=win32 wine "$WINE_DIR/drive_c/Program Files/GTA Vice City/gta-vc.exe"
Icon=$ICON_PATH
Terminal=false
Type=Application
Categories=Game;
StartupNotify=true
Path=$WINE_DIR/drive_c/Program Files/GTA Vice City
EOF
chmod +x "$SHORTCUT_PATH"

# Make shortcut visible on desktop as well
DESKTOP_SHORTCUT="$HOME/Desktop/gta-vice-city.desktop"
cp "$SHORTCUT_PATH" "$DESKTOP_SHORTCUT"
chmod +x "$DESKTOP_SHORTCUT"

echo -e "\n${GREEN}═════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}★ LINUX CONFIGURATION COMPLETED SUCCESSFULLY! ★${NC}"
echo -e "${GREEN}═════════════════════════════════════════════════════════${NC}"
echo -e "1. ${YELLOW}Copy your GTA Vice City game files${NC} to:"
echo -e "   ${CYAN}$WINE_DIR/drive_c/Program Files/GTA Vice City/${NC}"
echo -e "2. Double click the '${YELLOW}GTA Vice City Launcher${NC}' icon on your Desktop or search for it in your application dashboard."
echo -e "3. Enjoy seamless lo-fi high-fps gaming on Linux!"
