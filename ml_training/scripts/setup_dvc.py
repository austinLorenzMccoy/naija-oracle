"""
Setup DVC and DagsHub integration for Naija Oracle
"""

import os
import subprocess
import argparse
from pathlib import Path

def run_command(cmd: str, cwd: str = None) -> bool:
    """Run shell command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running command: {cmd}")
            print(f"Error: {result.stderr}")
            return False
        print(f"Success: {cmd}")
        return True
    except Exception as e:
        print(f"Exception running command: {cmd}")
        print(f"Error: {e}")
        return False

def setup_dvc_repo():
    """Initialize DVC repository"""
    print("Initializing DVC repository...")
    
    # Initialize DVC
    if not run_command("dvc init"):
        return False
    
    # Create DVC directories
    os.makedirs("data", exist_ok=True)
    os.makedirs("models", exist_ok=True)
    os.makedirs("metrics", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    
    # Add data directories to DVC
    run_command("dvc add data/persona_training_data.json")
    run_command("dvc add data/recommendation_training_data.csv")
    run_command("dvc add data/cvi_anchors.json")
    
    # Add models directory to DVC
    run_command("dvc add models/persona_simulator")
    run_command("dvc add models/recommendation_engine")
    
    return True

def setup_dagshub_remote(dagshub_username: str, dvc_token: str):
    """Setup DagsHub remote for DVC"""
    print(f"Setting up DagsHub remote for user: {dagshub_username}")
    
    # Set DVC token environment variable
    os.environ["DVC_TOKEN"] = dvc_token
    
    # Add DagsHub remote
    remote_url = f"dagsHub://{dagshub_username}/naija-oracle"
    if not run_command(f"dvc remote add -d origin {remote_url}"):
        return False
    
    # Configure authentication
    if not run_command(f'dvc remote modify origin username {dagshub_username}'):
        return False
    
    if not run_command('dvc remote modify origin password DVC_TOKEN'):
        return False
    
    return True

def setup_mlflow_tracking():
    """Setup MLflow tracking with DagsHub"""
    print("Setting up MLflow tracking...")
    
    # Create MLflow directory
    os.makedirs("mlruns", exist_ok=True)
    
    # Add MLflow to DVC (but exclude runs from tracking)
    with open(".dvcignore", "a") as f:
        f.write("\n# Exclude MLflow runs from DVC tracking\nmlruns/\n")
    
    return True

def create_dvc_pipeline():
    """Create DVC pipeline configuration"""
    print("Creating DVC pipeline...")
    
    # The dvc.yaml file was already created
    print("DVC pipeline configuration created in dvc.yaml")
    
    return True

def push_to_dagshub():
    """Push initial data and models to DagsHub"""
    print("Pushing to DagsHub...")
    
    # Push DVC tracked files
    if not run_command("dvc push"):
        print("Warning: DVC push failed, but this might be expected for initial setup")
    
    return True

def main():
    parser = argparse.ArgumentParser(description="Setup DVC and DagsHub for Naija Oracle")
    parser.add_argument("--dagshub-username", type=str, required=True, help="DagsHub username")
    parser.add_argument("--dvc-token", type=str, help="DVC token for authentication")
    parser.add_argument("--skip-push", action="store_true", help="Skip initial push to DagsHub")
    
    args = parser.parse_args()
    
    print("🚀 Setting up DVC and DagsHub for Naija Oracle ML Pipeline")
    print("=" * 60)
    
    # Change to ML training directory
    ml_dir = Path(__file__).parent.parent
    os.chdir(ml_dir)
    
    success = True
    
    # Setup DVC
    if not setup_dvc_repo():
        success = False
    
    # Setup DagsHub remote
    if args.dagshub_username and args.dvc_token:
        if not setup_dagshub_remote(args.dagshub_username, args.dvc_token):
            success = False
    else:
        print("⚠️  DagsHub credentials not provided. You'll need to set them up manually.")
        print("Run: dvc remote add -d origin dagsHub://your-username/naija-oracle")
    
    # Setup MLflow
    if not setup_mlflow_tracking():
        success = False
    
    # Create pipeline
    if not create_dvc_pipeline():
        success = False
    
    # Push to DagsHub
    if not args.skip_push and success:
        push_to_dagshub()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ DVC and DagsHub setup completed successfully!")
        print("\nNext steps:")
        print("1. Commit the changes to git:")
        print("   git add .")
        print("   git commit -m 'Add DVC and DagsHub integration'")
        print("   git push")
        print("\n2. Run your first DVC pipeline:")
        print("   dvc repro")
        print("\n3. Push data and models to DagsHub:")
        print("   dvc push")
    else:
        print("❌ Setup failed. Please check the error messages above.")
    
    print("\n📖 For more information, see:")
    print("- DVC documentation: https://dvc.org/doc")
    print("- DagsHub documentation: https://dagshub.com/docs")

if __name__ == "__main__":
    main()
