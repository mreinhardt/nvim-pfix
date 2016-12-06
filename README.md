A neovim plugin to search and replace across project files interactively.

## Overview

Based on the vim plugin `greplace` by Yegappan Lakshmanan
http://www.vim.org/scripts/script.php?script_id=1813

This plugin allows you to search and replace a pattern across all
project files. The lines containing a specified pattern are displayed
in a buffer. You can edit the lines in this buffer and make the
desired modifications to them. You can then incorporate these changes
back into the corresponding files interactively.

The following commands are provided by this plugin:

```
:Pfind           Search for a given pattern and display matches in the
                 replace buffer.
:Pfix            Use buffer modifications to replace the given lines
                 in the corresponding files.
```

Refer to [nvim-pfix.txt](doc/nvim-pfix.txt) for more information.

## Customization

To customize command used for `:Pfind` you can update both the command and
the default options.

  * [git grep](https://www.kernel.org/pub/software/scm/git/docs/git-grep.html)

        let g:nvim_pfix_pfind='git grep'
        let g:nvim_pfix_pfind_opts='--line-number'

  * [ack](http://beyondgrep.com/)

        let g:nvim_pfix_pfind='ack'
        let g:nvim_pfix_pfind_opts='--noheading'

  * [ag](https://github.com/ggreer/the_silver_searcher)

        let g:nvim_pfix_pfind='ag'
        let g:nvim_pfix_pfind_opts='--numbers --noheading'

  * [rg](https://github.com/BurntSushi/ripgrep)

        let g:nvim_pfix_pfind='rg'
        let g:nvim_pfix_pfind_opts='--line-number --no-heading'

