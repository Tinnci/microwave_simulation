use iced::{
    widget::{button, column, container, radio, row, scrollable, text, text_input, tooltip, Space},
    Alignment, Length, Renderer,
};

use crate::{MicrowaveGUI, MatchingMethod, Theme};

impl MicrowaveGUI {
    pub(crate) fn view_content(&self) -> iced::Element<'_, Message, Renderer<Theme>> {
        let title = text("微波阻抗匹配设计工具")
            .size(30)
            .width(Length::Fill)
            .horizontal_alignment(iced::alignment::Horizontal::Center);

        let matching_method = container(
            column![
                text("匹配方法").size(20),
                row![
                    radio(
                        "四分之一波长变换器",
                        MatchingMethod::QuarterWave,
                        Some(self.matching_method),
                        Message::MatchingMethodChanged
                    ),
                    Space::with_width(Length::Fixed(20.0)),
                    radio(
                        "单枝节匹配",
                        MatchingMethod::Stub,
                        Some(self.matching_method),
                        Message::MatchingMethodChanged
                    ),
                ]
                .spacing(10)
                .padding(10)
            ]
            .spacing(10)
            .padding(10)
        );

        let input_section = container(
            column![
                text("输入参数").size(20),
                row![
                    text("频率 (GHz):").width(Length::FillPortion(1)),
                    tooltip(
                        text_input("输入频率", &self.frequency)
                            .on_input(Message::FrequencyChanged)
                            .width(Length::FillPortion(2)),
                        "工作频率 (1-20 GHz)",
                        tooltip::Position::Bottom,
                    )
                ]
                .spacing(10),
                row![
                    text("负载阻抗实部 (Ω):").width(Length::FillPortion(1)),
                    tooltip(
                        text_input("输入实部", &self.z_load_real)
                            .on_input(Message::ZLoadRealChanged)
                            .width(Length::FillPortion(2)),
                        "负载阻抗实部 (20-200 Ω)",
                        tooltip::Position::Bottom,
                    )
                ]
                .spacing(10),
                row![
                    text("负载阻抗虚部 (Ω):").width(Length::FillPortion(1)),
                    tooltip(
                        text_input("输入虚部", &self.z_load_imag)
                            .on_input(Message::ZLoadImagChanged)
                            .width(Length::FillPortion(2)),
                        "负载阻抗虚部 (-200-200 Ω)",
                        tooltip::Position::Bottom,
                    )
                ]
                .spacing(10),
                row![
                    text("特征阻抗 (Ω):").width(Length::FillPortion(1)),
                    tooltip(
                        text_input("输入特征阻抗", &self.z0)
                            .on_input(Message::Z0Changed)
                            .width(Length::FillPortion(2)),
                        "特征阻抗 (20-200 Ω)",
                        tooltip::Position::Bottom,
                    )
                ]
                .spacing(10)
            ]
            .spacing(10)
            .padding(10)
        );

        let calculate_button = container(
            tooltip(
                button("计算")
                    .on_press(Message::Calculate)
                    .width(Length::Fill)
                    .padding(10),
                "计算匹配网络",
                tooltip::Position::Bottom,
            )
        )
        .width(Length::Fill)
        .padding(10);

        let result_section = if !self.result.is_empty() {
            container(
                text(&self.result)
                    .width(Length::Fill)
                    .horizontal_alignment(iced::alignment::Horizontal::Center)
            )
            .padding(10)
        } else {
            container(text("")).padding(0)
        };

        scrollable(
            column![
                title,
                Space::with_height(Length::Fixed(20.0)),
                matching_method,
                Space::with_height(Length::Fixed(20.0)),
                input_section,
                Space::with_height(Length::Fixed(20.0)),
                calculate_button,
                result_section,
            ]
            .spacing(10)
            .padding(20)
            .width(Length::Fill)
            .align_items(Alignment::Center)
        )
        .into()
    }
}

#[derive(Debug, Clone)]
pub enum Message {
    FrequencyChanged(String),
    ZLoadRealChanged(String),
    ZLoadImagChanged(String),
    Z0Changed(String),
    MatchingMethodChanged(MatchingMethod),
    Calculate,
} 