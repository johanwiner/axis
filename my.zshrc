# Set up the prompt

#autoload -Uz promptinit
#promptinit
#prompt walters

HISTSIZE=1000
SAVEHIST=1000
unsetopt beep

# Use emacs keybindings even if our EDITOR is set to vi
bindkey -e

# Keep 1000 lines of history within the shell and save it to ~/.zsh_history:
HISTSIZE=1000
SAVEHIST=1000
HISTFILE=~/.zsh_history

PROMPT="{%S%n%s@%m}%2~$"


precmd () { print -Pn "\e]2;%n@%M | %~\a" } 

autoload -z compinit
compinit

zstyle ':completion:*' auto-description 'specify: %d'
zstyle ':completion:*' completer _expand _complete _correct _approximate
zstyle ':completion:*' format 'Completing %d'
zstyle ':completion:*' group-name ''
zstyle ':completion:*' menu select=2
eval "$(dircolors -b)"
zstyle ':completion:*:default' list-colors ${(s.:.)LS_COLORS}
zstyle ':completion:*' list-colors ''
zstyle ':completion:*' list-prompt %SAt %p: Hit TAB for more, or the character to insert%s
zstyle ':completion:*' matcher-list '' 'm:{a-z}={A-Z}' 'm:{a-zA-Z}={A-Za-z}' 'r:|[._-]=* r:|=* l:|=*'
zstyle ':completion:*' menu select=long
zstyle ':completion:*' select-prompt %SScrolling active: current selection at %p%s
zstyle ':completion:*' use-compctl false
zstyle ':completion:*' verbose true

typeset -A key

key[Home]=${terminfo[khome]}
key[End]=${terminfo[kend]}
key[Insert]=${terminfo[kich1]}
key[Delete]=${terminfo[kdch1]}
key[Up]=${terminfo[kcuu1]}
key[Down]=${terminfo[kcud1]}
key[Left]=${terminfo[kcub1]}
key[Right]=${terminfo[kcuf1]}
key[PageUp]=${terminfo[kpp]}
key[PageDown]=${terminfo[knp]}

# setup key accordingly
[[ -n "${key[Home]}"    ]]  && bindkey  "${key[Home]}"    beginning-of-line
[[ -n "${key[End]}"     ]]  && bindkey  "${key[End]}"     end-of-line
[[ -n "${key[Insert]}"  ]]  && bindkey  "${key[Insert]}"  overwrite-mode
[[ -n "${key[Delete]}"  ]]  && bindkey  "${key[Delete]}"  delete-char
[[ -n "${key[Up]}"      ]]  && bindkey  "${key[Up]}"      up-line-or-history
[[ -n "${key[Down]}"    ]]  && bindkey  "${key[Down]}"    down-line-or-history
[[ -n "${key[Left]}"    ]]  && bindkey  "${key[Left]}"    backward-char
[[ -n "${key[Right]}"   ]]  && bindkey  "${key[Right]}"   forward-char

# Finally, make sure the terminal is in application mode, when zle is
# active. Only then are the values from $terminfo valid.
function zle-line-init () {
    echoti smkx
}
function zle-line-finish () {
    echoti rmkx
}
zle -N zle-line-init
zle -N zle-line-finish 

# GCC ARM Embedded
export PATH=$PATH:$HOME/bin/gcc-arm-none-eabi-5_4-2016q3/bin

# Proxy settings

export http_proxy="http://wwwproxy.se.axis.com:3128"
export https_proxy="http://wwwproxy.se.axis.com:3128"

alias git s="git status"
alias git co="git co"

alias gitka="gitk --all&"
alias ls='ls --color=auto'
alias gdb='gdb --silent'

#Git hooks
alias gerritmsghook='GIT=$(git rev-parse --show-toplevel) && test -d $GIT/.git/hooks.bak || { mv $GIT/.git/hooks{,.bak} && mkdir $GIT/.git/hooks && scp -p -P 29418 $USERNAME@gittools.se.axis.com:hooks/commit-msg $GIT/.git/hooks/; }'

alias ungerritmsghook='GIT=$(git rev-parse --show-toplevel) && test -d $GIT/.git/hooks.bak && rm -rf $GIT/.git/hooks && mv $GIT/.git/hooks{.bak,}'



# GCC ARM Embedded
export PATH=$PATH:/home/johanwi/bin/gcc-arm-none-eabi-5_3-2016q1/bin
export PATH=$PATH:/home/johanwi/bin

# Path to usefull scripts that I have written
export PATH=$PATH:/home/johanwi/bin/johans_script

#Path to sublime text 3
export PATH=$PATH:/home/johanwi/Programs/sublime_text_3
alias subl="sublime_text"

export AXIS_TOP_DIR=`command pwd`
export AXIS_DEVELOPER=y
export AXIS_TESTER=y
export AXIS_GDB_MIPS=gdb-mips
source ~/oe-setup/oe-setup.sh

#settings for less
LESS=dMqifR

