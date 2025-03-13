# LightSMTPClient
Light portable python writed SMTP client with simple UI

# Releases
- 13/03/2025 - V1.3
  - Attachments
  - Log optimization
  - Code documentation
- 06/11/2023 - V1.2
  - Starttls
  - Authentication
- 24/01/2023 - V1.1
  - Logs display
- 18/07/2022 - V1.0
  - Initial release

# Default config
- You can modify config.yml to set default values

# Build
```shell
pyinstaller --noconfirm --onefile --windowed --icon "icon.ico" --name "LightSMTPClient V1.3" --add-data "config.yml;."  "client.py"```
