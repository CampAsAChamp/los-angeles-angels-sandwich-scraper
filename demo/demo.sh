#!/usr/bin/env zsh

# Check if pr-reqs are installed, prior to running the demo
if ! which gum >/dev/null; then
    echo "You need 'gum' to run this demo. Installation instructions here: https://github.com/charmbracelet/gum#installation"
    exit 1
fi

if ! which cowsay >/dev/null; then
    echo "You need 'cowsay' to run this demo. Installation instructions here: https://letmegooglethat.com/?q=how+to+install+cowsay"
    exit 1
fi

if ! which lolcat >/dev/null; then
    echo "You need 'lolcat' to run this demo. Installation instructions here: https://github.com/busyloop/lolcat#installation"
    exit 1
fi

if ! which bat >/dev/null; then
    echo "You need 'bat' to run this demo. Installation instructions here: https://github.com/sharkdp/bat#installation"
    exit 1
fi

if ! which exa >/dev/null; then
    echo "You need 'exa' to run this demo. Installation instructions here: https://the.exa.website/"
    exit 1
fi

if ! which pytest >/dev/null; then
    echo "You need 'pytest' to run this demo. Installation instructions here: https://docs.pytest.org/en/7.4.x/"
    exit 1
fi

# if ! which playwright > /dev/null; then
#     echo "You need 'playwright' to run this demo. Installation instructions here: https://playwright.dev/"
#     exit 1
# fi

# Set variables
SCRIPT_SOURCE=$(dirname "${BASH_SOURCE[0]}")
export APP_URL="http://localhost:8000"

function cowecho() {
    local input="$1"
    cow=$(shuf -n 1 -e $(cowsay -l | perl -p -e 's/Cow files.*//'))
    echo "$input" | cowsay -f "$cow" | lolcat -a -t --duration 2
}

function gumbox() {
    local input="$1"
    gum style \
        --border normal --margin "1" \
        --padding "1 2" --border-foreground 212 \
        "${input}"
}

function gumtext() {
    local input="$1"
    gum style --foreground 212 "${input}"
}

function gumspin() {
    local type="$1"
    local input="$2"
    gum spin -s $type --title "${input}" -- sleep 5
}

function guminput() {
    local input="$1"
    gum input --placeholder "${input}"
}

# Introduction
gumbox "Hello! Welcome to $(gumtext 'The Self-Driven Demo about my Los Angeles Chick Fil A Scraper!')"
PROMPT=$(guminput "Press any button to continue...")

echo -e "$(gumtext "LET'S DO IT!")"

sleep 2
clear

cowecho "In this demo, we have a simple Python application that scrapes the Sports Reference website to see if the any of the games last night match the criteria for free Chick Fil A:"
cowecho "- Angels score 7 or more runs at home\n
- Ducks score 5 or more goals at home\n
- LAFC wins at home"
sleep 10

cowecho "It uses GitHub Actions to run automatically every day, but today we will be running it manually on my local machine"

PROMPT=$(guminput "Press any button to continue...")
clear

gumbox "I picked the $(gumtext 'Sports Reference') website for a few reasons"
sleep 4
echo -e "$(gumtext "+ Free (unlike any of the APIs)")"
sleep 4
echo -e "$(gumtext "+ The website is for information first, style is less important")"
sleep 4
echo -e "$(gumtext "+ Relatively light on CSS")"
sleep 4
echo -e "$(gumtext "+ Layout changes are very rare so my scraper won't break often and needs less maintence")"
sleep 4
echo -e "$(gumtext "+ Available for all major sports")"
sleep 4
echo
echo

imgcat demo/Angels_Schedule_Example.png
PROMPT=$(guminput "Press any button to continue...")
clear

echo -e "$(gumtext "The directory structure is quite simple for this demo 🗂️")"
exa src/ --git-ignore -T --color=always --group-directories-first --icons
PROMPT=$(guminput "Press any button to continue...")
clear

echo -e "$(gumtext "The application is a Python app whose main logic is this 👇")"
sleep 2
bat demo/example_main.py
PROMPT=$(guminput "Press any button to continue...")
clear

echo -e "$(gumtext "It sends emails using the built in SMTP library 👇")"
sleep 2
bat demo/example_messenger.py
PROMPT=$(guminput "Press any button to continue...")
clear

echo -e "$(gumtext "The dependencies for the app are as follows 👇")"
bat requirements.txt
PROMPT=$(guminput "Press any button to continue...")
clear

gumspin dot "We're now going to demo the application"
python src/main.py
PROMPT=$(guminput "Press any button to continue...")
clear

echo -e "$(gumtext "Then the final step is to set it up to run automatically on a schedule using GitHub Actions 👇")"
sleep 4
bat .github/workflows/github-actions.yaml
PROMPT=$(guminput "Press any button to continue...")
clear

code .

open https://github.com/CampAsAChamp/los-angeles-chick-fil-a-scraper

gumbox "Thank you for attending! Any questions?"
PROMPT=$(guminput "Press any button to continue...")