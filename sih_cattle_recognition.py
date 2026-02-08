"""
GOVANSH - Smart India Hackathon (SIH) Project

Backward-compatible launcher.

Recommended entrypoint:
  python run_govansh.py

You can still run:
  python sih_cattle_recognition.py
"""

from govansh_app.app import create_app


def main():
    app = create_app()
    app.run(debug=False, host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()

