#!/usr/bin/python
# encoding: utf-8

import sys

from workflow import Workflow

def main(wf):
    # The Workflow instance will be passed to the function
    # you call from `Workflow.run`. Not so useful, as
    # the `wf` object created in `if __name__ ...` below is global.
    #
    # Your imports go here if you want to catch import errors (not a bad idea)
    # or if the modules/packages are in a directory added via `Workflow(libraries=...)`
    # import somemodule
    
    # Get args from Workflow, already in normalized Unicode
    args = wf.args


    # Updates
    # ------------------------------------------------------------------
    if wf.update_available:
        wf.add_item('A newer version is available',
                    '↩ to install update',
                    autocomplete='workflow:update',
                    icon=ICON_UPDATE)

    # Add an item to Alfred feedback
    wf.add_item(u'Item title', u' '.join(args))

    # Send output to Alfred. You can only call this once.
    # Well, you *can* call it multiple times, but Alfred won't be listening
    # any more...
    wf.send_feedback()


if __name__ == '__main__':
    # Create a global `Workflow` object
    wf = Workflow(update_settings={
        'github_slug': 'joshuajharris/alfred-medium-workflow',
        'version': '0.1'
    })

    # Call your entry function via `Workflow.run()` to enable its helper
    # functions, like exception catching, ARGV normalization, magic
    # arguments etc.
    sys.exit(wf.run(main))
