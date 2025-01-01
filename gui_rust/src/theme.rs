use iced::{
    application,
    widget::{container, button, text_input, radio, text, scrollable},
    Color,
};

#[derive(Debug, Clone, Copy, Default, PartialEq, Eq)]
pub enum Theme {
    #[default]
    Light,
    Dark,
}

impl application::StyleSheet for Theme {
    type Style = ();

    fn appearance(&self, _style: &()) -> application::Appearance {
        match self {
            Theme::Light => application::Appearance {
                background_color: Color::WHITE,
                text_color: Color::BLACK,
            },
            Theme::Dark => application::Appearance {
                background_color: Color::from_rgb(0.1, 0.1, 0.1),
                text_color: Color::WHITE,
            },
        }
    }
}

impl container::StyleSheet for Theme {
    type Style = ();

    fn appearance(&self, _style: &()) -> container::Appearance {
        match self {
            Theme::Light => container::Appearance {
                text_color: Some(Color::BLACK),
                background: Some(iced::Background::Color(Color::from_rgb(0.95, 0.95, 0.95))),
                border_radius: 5.0.into(),
                border_width: 1.0,
                border_color: Color::from_rgb(0.8, 0.8, 0.8),
            },
            Theme::Dark => container::Appearance {
                text_color: Some(Color::WHITE),
                background: Some(iced::Background::Color(Color::from_rgb(0.15, 0.15, 0.15))),
                border_radius: 5.0.into(),
                border_width: 1.0,
                border_color: Color::from_rgb(0.3, 0.3, 0.3),
            },
        }
    }
}

impl button::StyleSheet for Theme {
    type Style = ();

    fn active(&self, _style: &()) -> button::Appearance {
        match self {
            Theme::Light => button::Appearance {
                shadow_offset: iced::Vector::new(0.0, 0.0),
                background: Some(iced::Background::Color(Color::from_rgb(0.9, 0.9, 0.9))),
                border_radius: 5.0.into(),
                border_width: 1.0,
                border_color: Color::from_rgb(0.7, 0.7, 0.7),
                text_color: Color::BLACK,
            },
            Theme::Dark => button::Appearance {
                shadow_offset: iced::Vector::new(0.0, 0.0),
                background: Some(iced::Background::Color(Color::from_rgb(0.2, 0.2, 0.2))),
                border_radius: 5.0.into(),
                border_width: 1.0,
                border_color: Color::from_rgb(0.4, 0.4, 0.4),
                text_color: Color::WHITE,
            },
        }
    }

    fn hovered(&self, style: &()) -> button::Appearance {
        let active = self.active(style);

        button::Appearance {
            shadow_offset: active.shadow_offset + iced::Vector::new(0.0, 1.0),
            ..active
        }
    }

    fn pressed(&self, style: &()) -> button::Appearance {
        button::Appearance {
            shadow_offset: iced::Vector::default(),
            ..self.active(style)
        }
    }

    fn disabled(&self, style: &()) -> button::Appearance {
        let active = self.active(style);

        button::Appearance {
            shadow_offset: iced::Vector::default(),
            background: active.background.map(|background| match background {
                iced::Background::Color(color) => iced::Background::Color(Color {
                    a: color.a * 0.5,
                    ..color
                }),
                iced::Background::Gradient(_) => background,
            }),
            text_color: Color {
                a: active.text_color.a * 0.5,
                ..active.text_color
            },
            ..active
        }
    }
}

impl text_input::StyleSheet for Theme {
    type Style = ();

    fn active(&self, _style: &()) -> text_input::Appearance {
        match self {
            Theme::Light => text_input::Appearance {
                background: iced::Background::Color(Color::WHITE),
                border_radius: 5.0.into(),
                border_width: 1.0,
                border_color: Color::from_rgb(0.7, 0.7, 0.7),
                icon_color: Color::from_rgb(0.7, 0.7, 0.7),
            },
            Theme::Dark => text_input::Appearance {
                background: iced::Background::Color(Color::from_rgb(0.15, 0.15, 0.15)),
                border_radius: 5.0.into(),
                border_width: 1.0,
                border_color: Color::from_rgb(0.3, 0.3, 0.3),
                icon_color: Color::from_rgb(0.7, 0.7, 0.7),
            },
        }
    }

    fn focused(&self, style: &()) -> text_input::Appearance {
        let active = self.active(style);

        text_input::Appearance {
            border_color: match self {
                Theme::Light => Color::from_rgb(0.5, 0.5, 0.5),
                Theme::Dark => Color::from_rgb(0.5, 0.5, 0.5),
            },
            ..active
        }
    }

    fn placeholder_color(&self, _style: &()) -> Color {
        match self {
            Theme::Light => Color::from_rgb(0.7, 0.7, 0.7),
            Theme::Dark => Color::from_rgb(0.5, 0.5, 0.5),
        }
    }

    fn value_color(&self, _style: &()) -> Color {
        match self {
            Theme::Light => Color::BLACK,
            Theme::Dark => Color::WHITE,
        }
    }

    fn selection_color(&self, _style: &()) -> Color {
        match self {
            Theme::Light => Color::from_rgb(0.8, 0.8, 1.0),
            Theme::Dark => Color::from_rgb(0.3, 0.3, 0.5),
        }
    }

    fn disabled(&self, style: &()) -> text_input::Appearance {
        let active = self.active(style);

        text_input::Appearance {
            background: match active.background {
                iced::Background::Color(color) => iced::Background::Color(Color {
                    a: color.a * 0.5,
                    ..color
                }),
                iced::Background::Gradient(_) => active.background,
            },
            ..active
        }
    }

    fn disabled_color(&self, _style: &()) -> Color {
        match self {
            Theme::Light => Color::from_rgb(0.7, 0.7, 0.7),
            Theme::Dark => Color::from_rgb(0.3, 0.3, 0.3),
        }
    }
}

impl radio::StyleSheet for Theme {
    type Style = ();

    fn active(&self, _style: &(), _is_selected: bool) -> radio::Appearance {
        match self {
            Theme::Light => radio::Appearance {
                background: iced::Background::Color(Color::WHITE),
                dot_color: Color::BLACK,
                border_width: 1.0,
                border_color: Color::from_rgb(0.7, 0.7, 0.7),
                text_color: Some(Color::BLACK),
            },
            Theme::Dark => radio::Appearance {
                background: iced::Background::Color(Color::from_rgb(0.15, 0.15, 0.15)),
                dot_color: Color::WHITE,
                border_width: 1.0,
                border_color: Color::from_rgb(0.3, 0.3, 0.3),
                text_color: Some(Color::WHITE),
            },
        }
    }

    fn hovered(&self, style: &(), is_selected: bool) -> radio::Appearance {
        let active = self.active(style, is_selected);

        radio::Appearance {
            border_color: match self {
                Theme::Light => Color::from_rgb(0.5, 0.5, 0.5),
                Theme::Dark => Color::from_rgb(0.5, 0.5, 0.5),
            },
            ..active
        }
    }
}

impl text::StyleSheet for Theme {
    type Style = ();

    fn appearance(&self, _style: ()) -> text::Appearance {
        match self {
            Theme::Light => text::Appearance {
                color: Some(Color::BLACK),
            },
            Theme::Dark => text::Appearance {
                color: Some(Color::WHITE),
            },
        }
    }
}

impl scrollable::StyleSheet for Theme {
    type Style = ();

    fn active(&self, _style: &()) -> scrollable::Scrollbar {
        match self {
            Theme::Light => scrollable::Scrollbar {
                background: Some(iced::Background::Color(Color::from_rgb(0.9, 0.9, 0.9))),
                border_radius: 5.0.into(),
                border_width: 0.0,
                border_color: Color::TRANSPARENT,
                scroller: scrollable::Scroller {
                    color: Color::from_rgb(0.7, 0.7, 0.7),
                    border_radius: 5.0.into(),
                    border_width: 0.0,
                    border_color: Color::TRANSPARENT,
                },
            },
            Theme::Dark => scrollable::Scrollbar {
                background: Some(iced::Background::Color(Color::from_rgb(0.2, 0.2, 0.2))),
                border_radius: 5.0.into(),
                border_width: 0.0,
                border_color: Color::TRANSPARENT,
                scroller: scrollable::Scroller {
                    color: Color::from_rgb(0.4, 0.4, 0.4),
                    border_radius: 5.0.into(),
                    border_width: 0.0,
                    border_color: Color::TRANSPARENT,
                },
            },
        }
    }

    fn hovered(&self, style: &(), is_mouse_over_scrollbar: bool) -> scrollable::Scrollbar {
        let active = self.active(style);

        if is_mouse_over_scrollbar {
            scrollable::Scrollbar {
                scroller: scrollable::Scroller {
                    color: match self {
                        Theme::Light => Color::from_rgb(0.5, 0.5, 0.5),
                        Theme::Dark => Color::from_rgb(0.6, 0.6, 0.6),
                    },
                    ..active.scroller
                },
                ..active
            }
        } else {
            active
        }
    }
} 