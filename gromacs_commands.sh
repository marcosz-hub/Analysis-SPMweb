#!/bin/bash

# remove pbc with gmx trjconv (you can change gromacs command for the one you need). 
# remember to have gromacs installed in your system or virtual environment.

for rep in r1 r2 r3 r4 r5; do #add as many replicas as you want

    # change "pattern" for your file names
    xtc="pattern_${rep}.xtc"
    tpr="pattern_${rep}.tpr"
    out="pattern_${rep}_nopbc.xtc"

    # Check if files exist
    if [[ ! -f "$xtc" || ! -f "$tpr" ]]; then
        echo "⚠️  $xtc or $tpr don't exit. Skipping ${rep}."
        continue
    fi

    echo "Processing ${rep}..."

    if echo "Complex" "Complex" "Complex" | gmx trjconv \
        -f "$xtc" \
        -s "$tpr" \
        -o "$out" \
        -pbc cluster \
        -ur compact \
        -center ; then
        
        echo "✅ $rep processed successfully"
    else
        echo "❌ Error in $rep. Skipping to next replica."
    fi

done

echo "➡️ Script finished."
finished."