use crate::MicrowaveGUI;
use pyo3::Python;
use std::time::Instant;
use super::initialize;

#[test]
fn test_batch_update_performance() {
    initialize();
    Python::with_gil(|_py| {
        let mut gui = MicrowaveGUI::default();
        let start = Instant::now();
        
        // 执行大量批量更新
        for i in 0..10000 {
            gui.begin_update();
            gui.set_frequency(format!("{}", i));
            gui.set_z0(format!("{}", i * 2));
            gui.set_load(format!("{}", i * 3));
            gui.end_update();
        }
        
        let duration = start.elapsed();
        println!("批量更新性能测试耗时: {:?}", duration);
        
        // 验证最终状态
        assert!(gui.state.frequency_valid);
        assert!(gui.state.z0_valid);
        assert!(gui.state.load_valid);
    });
}

#[test]
fn test_validation_performance() {
    initialize();
    Python::with_gil(|_py| {
        let mut gui = MicrowaveGUI::default();
        let start = Instant::now();
        
        // 执行大量验证操作
        for i in 0..10000 {
            gui.set_frequency(format!("{}.{}e9", i % 10, i % 5));
            assert!(gui.state.frequency_valid);
        }
        
        let duration = start.elapsed();
        println!("验证性能测试耗时: {:?}", duration);
    });
}

#[test]
fn test_theme_switching_performance() {
    initialize();
    Python::with_gil(|_py| {
        let mut gui = MicrowaveGUI::default();
        let start = Instant::now();
        
        // 执行大量主题切换
        for _ in 0..10000 {
            gui.set_theme("dark");
            gui.set_theme("light");
        }
        
        let duration = start.elapsed();
        println!("主题切换性能测试耗时: {:?}", duration);
    });
}

#[test]
fn test_concurrent_operations_performance() {
    initialize();
    Python::with_gil(|_py| {
        let mut gui = MicrowaveGUI::default();
        let start = Instant::now();
        
        // 执行大量并发操作
        for i in 0..1000 {
            gui.begin_update();
            gui.set_frequency(format!("{}", i));
            gui.set_z0(format!("{}", i));
            gui.set_load(format!("{}", i));
            gui.set_theme(if i % 2 == 0 { "light" } else { "dark" });
            gui.set_matching_method(if i % 5 == 0 { "L" } else if i % 5 == 1 { "Pi" } else { "T" });
            gui.end_update();
        }
        
        let duration = start.elapsed();
        println!("并发操作性能测试耗时: {:?}", duration);
    });
}

#[test]
fn test_memory_usage() {
    initialize();
    Python::with_gil(|_py| {
        let mut gui = MicrowaveGUI::default();
        
        // 创建大量字符串数据
        let mut data = Vec::new();
        for i in 0..10000 {
            data.push(format!("test_data_{}", i));
        }
        
        let start = Instant::now();
        
        // 测试内存使用
        for value in data {
            gui.set_result(value);
            gui.clear_result();
        }
        
        let duration = start.elapsed();
        println!("内存使用测试耗时: {:?}", duration);
    });
} 