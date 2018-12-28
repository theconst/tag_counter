#!/usr/bin/env python3
from model.db import dal

if __name__ == '__main__':
    import sys
    from tag_counter_controller import TagCounterController
    from model.tag_counter_model import TagCounterModel

    dal.db_init()
    model = TagCounterModel()

    if not sys.argv[1:]:
        from tk.tk_tag_counter_view import TkTagCounterView
        view = TkTagCounterView(model)
    else:
        from console.console_tag_counter_view import ConsoleTagCounterView
        view = ConsoleTagCounterView(model)

    TagCounterController(counter_view=view, counter_model=model).run()
