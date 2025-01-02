use pyo3::prelude::*;
use iced::{Application, Settings, Theme, window};

mod view;
use view::Message;

#[pyclass]
#[derive(Clone, Default)]
pub struct MicrowaveGUI {
    py_app: Option<PyObject>,
    matching_method: MatchingMethod,
    frequency: String,
    z_load_real: String,
    z_load_imag: String,
    z0: String,
    result: String,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub enum MatchingMethod {
    #[default]
    QuarterWave,
    Stub,
}

#[pymethods]
impl MicrowaveGUI {
    #[new]
    fn new(py_app: PyObject) -> Self {
        println!("Creating new MicrowaveGUI instance...");
        MicrowaveGUI {
            py_app: Some(py_app),
            matching_method: MatchingMethod::QuarterWave,
            frequency: String::new(),
            z_load_real: String::new(),
            z_load_imag: String::new(),
            z0: String::new(),
            result: String::new(),
        }
    }

    fn set_theme(&mut self, theme: &str) -> PyResult<()> {
        if let Some(ref py_app) = self.py_app {
            Python::with_gil(|py| {
                py_app.call_method1(py, "set_theme", (theme,))?;
                Ok(())
            })
        } else {
            Ok(())
        }
    }

    fn set_result(&mut self, result: String) -> PyResult<()> {
        self.result = result;
        Ok(())
    }

    fn validate_and_calculate(&mut self) -> PyResult<()> {
        if let Some(ref py_app) = self.py_app {
            Python::with_gil(|py| {
                let matching_method = match self.matching_method {
                    MatchingMethod::QuarterWave => "quarter_wave",
                    MatchingMethod::Stub => "stub",
                };

                let valid = py_app.call_method1(
                    py,
                    "validate_parameters",
                    (
                        &self.frequency,
                        &self.z0,
                        &self.z_load_real,
                        &self.z_load_imag,
                        matching_method,
                    ),
                )?;

                if valid.extract::<bool>(py)? {
                    if let Ok(result) = py_app.call_method0(py, "calculate") {
                        if let Ok(result_str) = result.extract::<String>(py) {
                            self.result = result_str;
                        }
                    }
                } else {
                    self.result = "参数无效，请检查输入".to_string();
                }
                Ok(())
            })
        } else {
            Ok(())
        }
    }
}

impl Application for MicrowaveGUI {
    type Message = Message;
    type Theme = Theme;
    type Executor = iced::executor::Default;
    type Flags = PyObject;

    fn new(py_app: PyObject) -> (Self, iced::Command<Message>) {
        println!("Creating new MicrowaveGUI instance from flags...");
        (
            MicrowaveGUI {
                py_app: Some(py_app),
                matching_method: MatchingMethod::QuarterWave,
                frequency: String::new(),
                z_load_real: String::new(),
                z_load_imag: String::new(),
                z0: String::new(),
                result: String::new(),
            },
            iced::Command::none()
        )
    }

    fn title(&self) -> String {
        String::from("微波阻抗匹配设计工具")
    }

    fn update(&mut self, message: Message) -> iced::Command<Message> {
        match message {
            Message::FrequencyChanged(value) => self.frequency = value,
            Message::ZLoadRealChanged(value) => self.z_load_real = value,
            Message::ZLoadImagChanged(value) => self.z_load_imag = value,
            Message::Z0Changed(value) => self.z0 = value,
            Message::MatchingMethodChanged(method) => self.matching_method = method,
            Message::Calculate => {
                if let Err(e) = self.validate_and_calculate() {
                    self.result = format!("计算错误: {}", e);
                }
            }
        }
        iced::Command::none()
    }

    fn view(&self) -> iced::Element<Message> {
        self.view_content()
    }

    fn theme(&self) -> Theme {
        Theme::default()
    }

    fn style(&self) -> <Theme as iced::application::StyleSheet>::Style {
        Default::default()
    }

    fn scale_factor(&self) -> f64 {
        1.0
    }
}

#[pyfunction]
fn start_gui(gui: &MicrowaveGUI) -> PyResult<()> {
    println!("Starting GUI...");
    let mut settings = Settings::with_flags(gui.py_app.as_ref().unwrap().clone());
    settings.window.size = (800, 600);
    settings.window.position = window::Position::Centered;
    settings.window.resizable = true;
    settings.window.decorations = true;
    settings.window.transparent = false;
    settings.antialiasing = true;

    MicrowaveGUI::run(settings)
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
}

#[pymodule]
fn microwave_gui(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<MicrowaveGUI>()?;
    m.add_function(wrap_pyfunction!(start_gui, m)?)?;
    Ok(())
}