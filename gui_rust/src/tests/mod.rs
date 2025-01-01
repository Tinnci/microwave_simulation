use pyo3::prelude::*;
use pretty_assertions::assert_eq as pretty_assert_eq;
use test_case::test_case;

pub mod theme_tests;
pub mod error_handling_tests;
pub mod python_interaction_tests;
pub mod performance_tests;

use std::sync::Once;

static INIT: Once = Once::new();

pub fn initialize() {
    INIT.call_once(|| {
        pyo3::prepare_freethreaded_python();
    });
}

#[cfg(test)]
mod tests {
    use crate::{MicrowaveGUI, Theme, MatchingMethod, ValidationState};
    use pyo3::Python;
    use super::initialize;

    #[test]
    fn test_gui_creation() {
        initialize();
        Python::with_gil(|_py| {
            let gui = MicrowaveGUI::default();
            assert_eq!(gui.frequency, "");
            assert_eq!(gui.z0, "");
            assert_eq!(gui.load, "");
        });
    }

    #[test]
    fn test_input_validation() {
        initialize();
        Python::with_gil(|_py| {
            let mut gui = MicrowaveGUI::default();
            
            // Test valid frequency
            gui.set_frequency("2.4e9".to_string());
            assert_eq!(gui.frequency, "2.4e9");
            
            // Test invalid frequency
            gui.set_frequency("invalid".to_string());
            assert_eq!(gui.frequency, "2.4e9"); // Should keep old value
        });
    }

    #[test]
    fn test_matching_method_selection() {
        initialize();
        Python::with_gil(|_py| {
            let mut gui = MicrowaveGUI::default();
            
            gui.set_matching_method("L");
            assert_eq!(gui.matching_method, MatchingMethod::L);
            
            gui.set_matching_method("Pi");
            assert_eq!(gui.matching_method, MatchingMethod::Pi);
            
            gui.set_matching_method("T");
            assert_eq!(gui.matching_method, MatchingMethod::T);
        });
    }

    #[test]
    fn test_theme_switching() {
        initialize();
        Python::with_gil(|_py| {
            let mut gui = MicrowaveGUI::default();
            assert_eq!(gui.theme, Theme::Light);
            
            gui.set_theme("dark");
            assert_eq!(gui.theme, Theme::Dark);
            
            gui.set_theme("light");
            assert_eq!(gui.theme, Theme::Light);
        });
    }

    #[test]
    fn test_validation_state() {
        initialize();
        Python::with_gil(|_py| {
            let mut state = ValidationState::default();
            assert!(!state.is_valid());
            
            state.frequency_valid = true;
            state.z0_valid = true;
            state.load_valid = true;
            assert!(state.is_valid());
            
            state.frequency_valid = false;
            assert!(!state.is_valid());
        });
    }
} 