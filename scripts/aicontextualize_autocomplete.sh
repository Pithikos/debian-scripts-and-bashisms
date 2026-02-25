_aicontextualize_complete() {
    local cur="${COMP_WORDS[COMP_CWORD]}"

    # Get the part after the last comma
    local prefix="${cur%,*}"
    local typing="${cur##*,}"

    # Generate file/dir completions for the current fragment
    local matches
    matches=$(compgen -f -- "$typing")

    # Re-attach the prefix (everything before last comma)
    local results=()
    while IFS= read -r match; do
        [[ -z "$match" ]] && continue
        if [[ "$cur" == *,* ]]; then
            results+=("${prefix},${match}")
        else
            results+=("$match")
        fi
    done <<< "$matches"

    COMPREPLY=("${results[@]}")
    compopt -o nospace 2>/dev/null
}

complete -F _aicontextualize_complete aicontextualize.py
