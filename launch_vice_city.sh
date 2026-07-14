#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════
#  GTA VICELAUNCHER — Native Linux Runner & Mod Integrator
#  Version 1.0  |  Powered by Mauxx AI
# ═══════════════════════════════════════════════════════════════════════

# ── Branding & Color Codes ─────────────────────────────────────────────
RED='\033[0;31m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'
GREEN='\033[0;32m'; PURPLE='\033[0;35m'; BOLD='\033[1m'; RESET='\033[0m'

print_banner() {
  echo -e "${RED}"
  echo "  ██████╗ ████████╗ █████╗     ██╗   ██╗██╗ ██████╗███████╗"
  echo "  ██╔════╝╚══██╔══╝██╔══██╗    ██║   ██║██║██╔════╝██╔════╝"
  echo "  ██║  ███╗  ██║   ███████║    ██║   ██║██║██║     █████╗  "
  echo "  ██║   ██║  ██║   ██╔══██║    ╚██╗ ██╔╝██║██║     ██╔══╝  "
  echo "  ╚██████╔╝  ██║   ██║  ██║     ╚████╔╝ ██║╚██████╗███████╗"
  echo "   ╚═════╝   ╚═╝   ╚═╝  ╚═╝      ╚═══╝  ╚═╝ ╚═════╝╚══════╝"
  echo -e "${YELLOW}"
  echo "         ★ NATIVE LINUX RUNNER & MOD SUITE SUITE ★"
  echo -e "${RESET}"
  echo -e "  ${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
  echo -e "  ${BOLD}${PURPLE}  ⚡ POWERED BY MAUXX AI — MAXIMUM PERFORMANCE DXVK GRAPHICS MAPPING${RESET}"
  echo -e "  ${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
  echo ""
}

log_info()    { echo -e "  ${CYAN}[ℹ]${RESET} $1"; }
log_ok()      { echo -e "  ${GREEN}[✓]${RESET} $1"; }
log_warn()    { echo -e "  ${YELLOW}[⚠]${RESET} $1"; }
log_error()   { echo -e "  ${RED}[✗]${RESET} $1"; }
log_step()    { echo -e "\n  ${BOLD}${YELLOW}▶ $1${RESET}"; }
log_launch()  { echo -e "  ${BOLD}${PURPLE}🚀 $1${RESET}"; }

# ── Configuration & Paths ──────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WINEPREFIX_DIR="${HOME}/.local/share/wineprefixes/gta-vice-city"
GAME_DIR="${WINEPREFIX_DIR}/drive_c/Program Files/GTA Vice City"
TRAINER_SCRIPT="${SCRIPT_DIR}/vice_cheats_trainer.py"
PLAY_URL="https://rajmodi135.github.io/vice-city-launcher/game/index.html"

# ── Main Entry ─────────────────────────────────────────────────────────
clear
print_banner

# ── 1. Check Wine Installation ──
log_step "Checking Wine Environment..."
if ! command -v wine &>/dev/null; then
  log_error "Wine is not installed! Please run 'sudo apt install wine' or check your package manager."
  exit 1
fi
log_ok "Wine binary found: $(wine --version)"

# ── 2. Check and Launch Background Trainer ──
if [ -f "$TRAINER_SCRIPT" ]; then
  log_step "Launching Python Cheat Trainer..."
  python3 "$TRAINER_SCRIPT" > /dev/null 2>&1 &
  log_ok "Trainer daemon spawned in the background."
else
  log_warn "Python Trainer script not found at: $TRAINER_SCRIPT"
fi

# ── 3. Launch Local Web Emulator ──
log_step "Opening Local Web Play Companion..."
log_launch "Loading: ${PLAY_URL}"
xdg-open "$PLAY_URL" > /dev/null 2>&1 &

# ── 4. Locate and Run Native GTA Vice City ──
log_step "Booting Native Engine Wrapper..."
if [ -f "${GAME_DIR}/gta-vc.exe" ]; then
  log_ok "Native Vice City executable detected at: ${GAME_DIR}/gta-vc.exe"
  log_launch "Starting native runtime wrapper with WINEPREFIX..."
  
  # Configure Wine prefix and run the game
  export WINEPREFIX="$WINEPREFIX_DIR"
  cd "$GAME_DIR" || exit 1
  wine gta-vc.exe > /dev/null 2>&1 &
  log_ok "Native game running. Keep this terminal open to preserve background modules."
else
  log_info "Native executable not found at standard path: ${GAME_DIR}/gta-vc.exe"
  log_info "No problem! You can play directly online in the opened browser tab."
fi

echo -e "\n  ${BOLD}${GREEN}★ Enjoy Playing Vice City with GTA VICELAUNCHER! ★${RESET}\n"
