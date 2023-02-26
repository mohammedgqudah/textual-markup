from .terminal_output import TerminalOutput
from ui.screen import Screen
from ui.styles import Styles, Display, Padding, DisplayType
from ui.static import Static
from ui.text import Text
from ui.button import Button
from ui.line_break import LineBreak


class TestUI(TerminalOutput):
    def test_it_renders_text(self):
        screen = Screen([
            Text("Hello world")
        ])
        assert "Hello world" == self.output(screen=screen).strip()

    def test_it_renders_text_on_the_next_line_by_default(self):
        screen = Screen([
            Text("Hello world"), Text("Testing")
        ])
        assert self.lines_as_string(
            self.line('Hello world'),
            self.line('Testing')
        ).strip() == self.output(screen=screen).strip()

    def test_it_renders_text_inline(self):
        inline = Styles(display=Display(type=DisplayType.INLINE_BLOCK))
        screen = Screen([
            Static(
                [
                    Text("Hello world", styles=inline),
                    Text("Testing", styles=inline)
                ]
            )
        ])
        assert """Hello worldTesting""" == self.output(screen=screen).strip()

    def test_styles_min_width(self):
        inline_display = Display(type=DisplayType.INLINE_BLOCK)
        screen = Screen().append(
            Static([
                Static([Text("Hello world")], styles=Styles(display=inline_display, min_width=14)),
                Static([Text("Testing")], styles=Styles(display=inline_display))
            ])
        )
        assert """Hello world  Testing""" == self.output(screen=screen).strip()

        screen = Screen([
            Static([
                Static([Text("Hello world")], styles=Styles(display=inline_display, min_width=5)),
                Static([Text("Testing")], styles=Styles(display=inline_display))
            ])
        ])
        assert """Hello worldTesting""" == self.output(screen=screen).strip()

    def test_styles_min_height(self):
        screen = Screen().append(
            Static([
                Static([Text("Hello world")], styles=Styles(min_height=4)),
                Static([Text("Testing")])
            ])
        )
        assert self.lines_as_string(
            self.line('Hello world'),
            self.lines(3),
            self.line("Testing")
        ).strip() == self.output(screen=screen).strip()

        screen = Screen([
            Static([
                Static([Text("Hello world")], styles=Styles(min_height=1)),
                Static([Text("Testing")])
            ])
        ])
        assert self.lines_as_string(
            self.line('Hello world'),
            self.line('Testing')
        ).strip() == self.output(screen=screen).strip()

    def test_nested_layout(self):
        screen = Screen([
            Static(
                [
                    Text("Title"),
                    Text("2", styles=Styles(display=Display(type=DisplayType.INLINE_BLOCK))),
                    Button("click me! ↗",
                           styles=Styles(display=Display(type=DisplayType.INLINE_BLOCK), padding=Padding())),
                    Text("3", styles=Styles(display=Display(type=DisplayType.INLINE_BLOCK))),
                    LineBreak(0),
                    Static([
                        Text("Hello")
                    ],
                        styles=Styles(display=Display(type=DisplayType.INLINE_BLOCK))
                    ),
                    Static([
                        Text("\tI'm nested"),
                        Static([
                            Text("\t\tmore nesting\ntest"),
                            Static([
                                Text("deep"),
                                Text("down"),
                            ])
                        ], styles=Styles(min_width=40))
                    ], id='second-static',
                        styles=Styles(min_height=20, min_width=60, display=Display(type=DisplayType.INLINE_BLOCK)))
                ],
                id='main-static', styles=Styles(min_height=20))
        ])

        assert self.lines_as_string(
            self.line('Title'),
            self.line('2click me! ↗3'),
            self.line("Hello        I'm nested"),
            self.line('                     more nesting'),
            self.line('     test'),
            self.line('     deep'),
            self.line('     down'),
        ).strip() == self.output(screen=screen).strip()
