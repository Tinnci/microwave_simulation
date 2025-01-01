use pyo3::Python;
use crate::{MicrowaveGUI, Message, MatchingMethod};

impl MicrowaveGUI {
    pub(crate) fn update(&mut self, message: Message) {
        match message {
            Message::FrequencyChanged(value) => {
                self.frequency = value;
                Python::with_gil(|py| {
                    let _ = self.py_app.call_method1(py, "set_frequency", (self.frequency.clone(),));
                });
            }
            Message::Z0Changed(value) => {
                self.z0 = value;
                Python::with_gil(|py| {
                    let _ = self.py_app.call_method1(py, "set_z0", (self.z0.clone(),));
                });
            }
            Message::ZLoadRealChanged(value) => {
                self.z_load_real = value;
                Python::with_gil(|py| {
                    let _ = self.py_app.call_method1(py, "set_z_load_real", (self.z_load_real.clone(),));
                });
            }
            Message::ZLoadImagChanged(value) => {
                self.z_load_imag = value;
                Python::with_gil(|py| {
                    let _ = self.py_app.call_method1(py, "set_z_load_imag", (self.z_load_imag.clone(),));
                });
            }
            Message::MatchingMethodChanged(method) => {
                self.matching_method = method;
                Python::with_gil(|py| {
                    let method_str = match self.matching_method {
                        MatchingMethod::QuarterWave => "quarter_wave",
                        MatchingMethod::Stub => "stub",
                    };
                    let _ = self.py_app.call_method1(py, "set_matching_method", (method_str,));
                });
            }
            Message::Calculate => {
                Python::with_gil(|py| {
                    if let Ok(result) = self.py_app.call_method0(py, "calculate") {
                        if let Ok(result_str) = result.extract::<String>(py) {
                            self.result = result_str;
                        }
                    }
                });
            }
        }
    }
} 