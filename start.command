#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
#  SafeAI Clinical Guidelines Assistant
#  Double-click this file to start. Everything is handled automatically.
# ─────────────────────────────────────────────────────────────────────────────

# Always run from the folder this script lives in
cd "$(dirname "$0")"

echo ""
echo "============================================================"
echo "   SafeAI — Clinical Guidelines Assistant"
echo "============================================================"
echo ""

# ── 1. Create virtual environment if it doesn't exist yet ────────────────────
if [ ! -d "safeai-env" ]; then
    echo "First-time setup: creating environment..."
    python3 -m venv safeai-env
    echo ""
fi

source safeai-env/bin/activate

# ── 2. Install packages if not already installed ─────────────────────────────
if ! python3 -c "import sentence_transformers" 2>/dev/null; then
    echo "First-time setup: installing packages (2-5 minutes)..."
    echo "Please wait — do not close this window."
    echo ""
    pip install -r requirements-pipeline.txt --quiet
    echo "Packages ready."
    echo ""
fi

# ── 3. If no knowledge base exists yet, process a PDF first ──────────────────
UGANDA_KB="extraction_output_uganda/knowledge_base.json"
MALARIA_KB="extraction_output_malaria/knowledge_base.json"

if [ ! -f "$UGANDA_KB" ] && [ ! -f "$MALARIA_KB" ]; then
    echo "No guideline has been processed yet."
    echo "Let's get your guideline set up — this only needs to happen once."
    echo ""

    # Open a native Mac file-picker so the user can click their PDF
    PDF_PATH=$(osascript -e 'POSIX path of (choose file with prompt "Select your clinical guideline PDF:" of type {"pdf"})' 2>/dev/null)

    # Fallback to typed path if the file-picker fails
    if [ -z "$PDF_PATH" ]; then
        echo "Could not open file picker. Please type the full path to your PDF:"
        read -p "> " PDF_PATH
    fi

    PDF_PATH=$(echo "$PDF_PATH" | tr -d '\n\r')

    if [ -z "$PDF_PATH" ] || [ ! -f "$PDF_PATH" ]; then
        echo ""
        echo "File not found. Please restart and try again."
        read -p "Press Enter to close..."
        exit 1
    fi

    echo ""
    echo "Which guideline is this?"
    echo ""
    echo "  1.  Uganda Clinical Guidelines"
    echo "  2.  WHO Malaria / iCCM Guidelines"
    echo "  3.  Other clinical PDF"
    echo ""
    read -p "Enter 1, 2, or 3: " CHOICE

    case $CHOICE in
        1) PRESET="--preset uganda" ;;
        2) PRESET="--preset who-malaria" ;;
        *) PRESET="" ;;
    esac

    echo ""
    echo "Processing your guideline — this takes 5 to 15 minutes the first time."
    echo "Please wait and do not close this window."
    echo ""

    python3 run_pipeline.py $PRESET --pdf "$PDF_PATH"

    if [ $? -ne 0 ]; then
        echo ""
        echo "Something went wrong during processing."
        echo "Please check the error above and try again."
        read -p "Press Enter to close..."
        exit 1
    fi

    echo ""
    echo "Guideline processed successfully!"
    echo ""
fi

# ── 4. Start the chat ─────────────────────────────────────────────────────────
python3 chat.py

echo ""
read -p "Press Enter to close..."
