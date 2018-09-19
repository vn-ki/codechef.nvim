# codechef.vim

A nvim plugin for codechef.

Depends on `fzf.vim` for selection window.

## Installation

```viml
Plug 'vn-ki/codechef.nvim'

Plug 'junegunn/fzf', { 'dir': '~/.fzf', 'do': './install --all' }
Plug 'junegunn/fzf.vim'
```

Don't forget to do `:UpdateRemotePlugins` after installation.

## Usage

- `:CodechefSelectContest` brings up an fzf window where you can select contests.
- After selecting a contest, press `o` on a problem to open it.
- Press `b` to go back.
