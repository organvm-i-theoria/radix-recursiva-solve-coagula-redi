#!/bin/bash

echo "🔧 Starting your essential terminal setup..."

# Install Homebrew (if not installed)
if ! command -v brew &>/dev/null; then
  echo "🧪 Installing Homebrew..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

echo "📦 Installing essential CLI tools..."

brew install zsh
brew install fzf
brew install bat
brew install eza
brew install tree
brew install fd
brew install ripgrep
brew install htop
brew install jq
brew install yq
brew install glow
brew install git
brew install gh
brew install rsync
brew install zoxide
brew install pyenv
brew install pipx
brew install poetry
brew install pre-commit
brew install tmux
brew install direnv
brew install watch
brew install nvm
brew install imagemagick
brew install ffmpeg
brew install sox

pipx ensurepath

# Optional: install oh-my-zsh
if [ ! -d "$HOME/.oh-my-zsh" ]; then
  echo "🎨 Installing oh-my-zsh..."
  sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
fi

echo "✅ All tools installed. Consider restarting your terminal to load changes."