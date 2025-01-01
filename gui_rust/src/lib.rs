use pyo3::prelude::*;
use std::fmt;

#[cfg(test)]
mod tests;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Theme {
    Light,
    Dark,
}

impl Default for Theme {
    fn default() -> Self {
        Theme::Light
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum MatchingMethod {
    L,
    Pi,
    T,
    QuarterWave,
    Stub,
}

impl Default for MatchingMethod {
    fn default() -> Self {
        MatchingMethod::L
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ValidationState {
    pub frequency_valid: bool,
    pub z0_valid: bool,
    pub load_valid: bool,
}

impl Default for ValidationState {
    fn default() -> Self {
        Self {
            frequency_valid: false,
            z0_valid: false,
            load_valid: false,
        }
    }
}

impl ValidationState {
    pub fn is_valid(&self) -> bool {
        self.frequency_valid && self.z0_valid && self.load_valid
    }
}

#[pyclass]
pub struct MicrowaveGUI {
    pub frequency: String,
    pub z0: String,
    pub load: String,
    pub matching_method: MatchingMethod,
    pub theme: Theme,
    pub result: String,
    pub error: String,
    pub state: ValidationState,
    pub py_app: Option<PyObject>,
}

#[pymethods]
impl MicrowaveGUI {
    #[new]
    fn new(py_app: PyObject) -> Self {
        Self {
            frequency: String::new(),
            z0: String::new(),
            load: String::new(),
            matching_method: MatchingMethod::default(),
            theme: Theme::default(),
            result: String::new(),
            error: String::new(),
            state: ValidationState::default(),
            py_app: Some(py_app),
        }
    }

    fn begin_update(&mut self) {
        if let Some(ref py_app) = self.py_app {
            Python::with_gil(|py| {
                let _ = py_app.call_method1(py, "record_call", ("begin_update",));
            });
        }
    }

    fn end_update(&mut self) {
        if let Some(ref py_app) = self.py_app {
            Python::with_gil(|py| {
                let _ = py_app.call_method1(py, "record_call", ("end_update",));
            });
        }
    }

    fn set_frequency(&mut self, value: String) {
        // 验证频率格式
        if let Ok(freq) = value.parse::<f64>() {
            if freq >= 0.0 {
                self.frequency = value;
                self.state.frequency_valid = true;
            } else {
                self.state.frequency_valid = false;
            }
        } else {
            self.state.frequency_valid = false;
        }
    }

    fn set_z0(&mut self, value: String) {
        // 验证阻抗格式
        if let Ok(z0) = value.parse::<f64>() {
            if z0 > 0.0 {
                self.z0 = value;
                self.state.z0_valid = true;
            } else {
                self.state.z0_valid = false;
            }
        } else {
            self.state.z0_valid = false;
        }
    }

    fn set_load(&mut self, value: String) {
        // 验证负载格式
        if let Ok(load) = value.parse::<f64>() {
            if load > 0.0 {
                self.load = value;
                self.state.load_valid = true;
            } else {
                self.state.load_valid = false;
            }
        } else {
            self.state.load_valid = false;
        }
    }

    fn set_matching_method(&mut self, value: &str) {
        match value {
            "L" => self.matching_method = MatchingMethod::L,
            "Pi" => self.matching_method = MatchingMethod::Pi,
            "T" => self.matching_method = MatchingMethod::T,
            "quarter_wave" => self.matching_method = MatchingMethod::QuarterWave,
            "stub" => self.matching_method = MatchingMethod::Stub,
            _ => {} // 保持当前值
        }
    }

    fn set_theme(&mut self, value: &str) {
        match value {
            "light" => self.theme = Theme::Light,
            "dark" => self.theme = Theme::Dark,
            _ => {} // 保持当前值
        }
    }

    fn set_result(&mut self, value: String) {
        self.result = value;
    }

    fn clear_result(&mut self) {
        self.result.clear();
    }

    fn set_error(&mut self, value: String) {
        self.error = value;
    }

    fn clear_error(&mut self) {
        self.error.clear();
    }
}

impl Default for MicrowaveGUI {
    fn default() -> Self {
        Self {
            frequency: String::new(),
            z0: String::new(),
            load: String::new(),
            matching_method: MatchingMethod::default(),
            theme: Theme::default(),
            result: String::new(),
            error: String::new(),
            state: ValidationState::default(),
            py_app: None,
        }
    }
}