#!/usr/bin/env bash

ROOT_DIR=$PWD

function start_ngrok {
  ngrok http 0.0.0.0:7010
}

function build {
  docker compose build
}

function up {
  docker compose up --remove-orphans 
}

function connect_to_backend {
  docker compose exec backend bash
}

function connect_to_frontend {
  docker compose exec frontend bash
}

function help {
  printf "$0 <task> [args]\n"
  printf "\nTasks:\n"
  compgen -A function | grep -v "^_" | cat -n
  printf '\nOther utility tasks are in the tools directory\n'
  printf "\n"
}

${@:-help}
