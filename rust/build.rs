use std::fs;
use std::path::Path;

fn main() {
    // Read the shared VERSION file from the project root (one level up from rust/)
    let version_path = Path::new("..").join("VERSION");
    let version = fs::read_to_string(&version_path)
        .expect("Could not read VERSION file")
        .trim()
        .to_string();

    println!("cargo:rustc-env=APP_VERSION={}", version);
    // Re-run build script if VERSION changes
    println!("cargo:rerun-if-changed=../VERSION");
}
