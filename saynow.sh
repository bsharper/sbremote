#!/bin/bash
read -r -d '' VOICES <<- EOM
Alex
Daniel
Fred
Karen
Moira
Rishi
Samantha
Tessa
Veena
Victoria
EOM
DT=$(date +%k)
TAILTXT=""
if [[ $(($(($RANDOM%10))%2)) == 1 ]]; then
  TAILTXT=", you got skipped"
fi
if [[ $DT -gt 8 && $DT -lt 23 ]]; then
  v=$(echo "$VOICES" | sort -R | tail -1)
  say -v "$v" "Move off ${1}${TAILTXT}" & 
fi
