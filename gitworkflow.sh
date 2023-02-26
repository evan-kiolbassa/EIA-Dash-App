#!/bin/bash
function stage_changes() {
    git add .
}

function commit_changes() {
    # Accepts a commit string as argument
    git commit -m "$1"
}

function push_changes() {
    git push origin
}

function set_remote_origin() {
    # Accepts a URL as argument

    if [[ $# -ne 1 ]]; then
        echo "Usage: set_remote_origin <remote_url>"
        return 1
    fi

    git remote add origin "$1"
}

