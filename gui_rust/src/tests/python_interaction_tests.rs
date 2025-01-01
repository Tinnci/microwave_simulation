use crate::{MicrowaveGUI, Theme, MatchingMethod};
use pyo3::prelude::*;
use std::sync::Arc;
use super::initialize;

// 模拟 Python 应用程序
#[pyclass]
struct MockPyApp {
    calls: Arc<std::sync::Mutex<Vec<String>>>,
}

#[pymethods]
impl MockPyApp {
    #[new]
    fn new() -> Self {
        Self {
            calls: Arc::new(std::sync::Mutex::new(Vec::new())),
        }
    }

    fn record_call(&self, method: &str) {
        let mut calls = self.calls.lock().unwrap();
        calls.push(method.to_string());
    }

    fn get_calls(&self) -> Vec<String> {
        let calls = self.calls.lock().unwrap();
        calls.clone()
    }
}

#[test]
fn test_py_app_initialization() {
    initialize();
    Python::with_gil(|py| {
        let app = Py::new(py, MockPyApp::new()).unwrap();
        let app_obj: PyObject = app.into_py(py);
        let gui = MicrowaveGUI::new(app_obj);
        assert!(gui.py_app.is_some());
    });
}

#[test]
fn test_py_app_interaction() {
    initialize();
    Python::with_gil(|py| {
        let app = Py::new(py, MockPyApp::new()).unwrap();
        let app_obj: PyObject = app.clone().into_py(py);
        let mut gui = MicrowaveGUI::new(app_obj);
        
        gui.begin_update();
        gui.set_frequency("2.4e9".to_string());
        gui.end_update();
        
        let mock_app = app.borrow(py);
        let calls = mock_app.get_calls();
        assert!(calls.contains(&"begin_update".to_string()));
        assert!(calls.contains(&"end_update".to_string()));
    });
}

#[test]
fn test_py_error_handling() {
    initialize();
    Python::with_gil(|py| {
        let app = Py::new(py, MockPyApp::new()).unwrap();
        let app_obj: PyObject = app.into_py(py);
        let mut gui = MicrowaveGUI::new(app_obj);
        
        gui.set_error("test error".to_string());
        assert_eq!(gui.error, "test error");
        
        gui.clear_error();
        assert_eq!(gui.error, "");
    });
}

#[test]
fn test_py_state_synchronization() {
    initialize();
    Python::with_gil(|py| {
        let app = Py::new(py, MockPyApp::new()).unwrap();
        let app_obj: PyObject = app.into_py(py);
        let mut gui = MicrowaveGUI::new(app_obj);
        
        gui.begin_update();
        gui.set_frequency("2.4e9".to_string());
        gui.set_z0("50".to_string());
        gui.end_update();
        
        assert_eq!(gui.frequency, "2.4e9");
        assert_eq!(gui.z0, "50");
    });
}

#[test]
fn test_py_calculation_interaction() {
    initialize();
    Python::with_gil(|py| {
        let app = Py::new(py, MockPyApp::new()).unwrap();
        let app_obj: PyObject = app.into_py(py);
        let mut gui = MicrowaveGUI::new(app_obj);
        
        gui.set_frequency("2.4e9".to_string());
        gui.set_z0("50".to_string());
        gui.set_matching_method("L");
        
        assert_eq!(gui.frequency, "2.4e9");
        assert_eq!(gui.z0, "50");
        assert_eq!(gui.matching_method, MatchingMethod::L);
    });
}

#[test]
fn test_py_theme_interaction() {
    initialize();
    Python::with_gil(|py| {
        let app = Py::new(py, MockPyApp::new()).unwrap();
        let app_obj: PyObject = app.into_py(py);
        let mut gui = MicrowaveGUI::new(app_obj);
        
        gui.set_theme("dark");
        assert_eq!(gui.theme, Theme::Dark);
        
        gui.set_theme("light");
        assert_eq!(gui.theme, Theme::Light);
    });
}

#[test]
fn test_py_validation_interaction() {
    initialize();
    Python::with_gil(|py| {
        let app = Py::new(py, MockPyApp::new()).unwrap();
        let app_obj: PyObject = app.into_py(py);
        let mut gui = MicrowaveGUI::new(app_obj);
        
        // 测试有效输入
        gui.set_frequency("2.4e9".to_string());
        assert_eq!(gui.frequency, "2.4e9");
        
        // 测试无效输入
        gui.set_frequency("invalid".to_string());
        assert_eq!(gui.frequency, "2.4e9"); // 应保持旧值
    });
}

#[test]
fn test_py_concurrent_interaction() {
    initialize();
    Python::with_gil(|py| {
        let app = Py::new(py, MockPyApp::new()).unwrap();
        let app_obj: PyObject = app.into_py(py);
        let mut gui = MicrowaveGUI::new(app_obj);
        
        // 测试并发更新
        gui.begin_update();
        gui.set_frequency("2.4e9".to_string());
        gui.set_z0("50".to_string());
        gui.end_update();
        
        gui.begin_update();
        gui.set_matching_method("L");
        gui.set_theme("dark");
        gui.end_update();
        
        assert_eq!(gui.frequency, "2.4e9");
        assert_eq!(gui.z0, "50");
        assert_eq!(gui.matching_method, MatchingMethod::L);
        assert_eq!(gui.theme, Theme::Dark);
    });
} 