# Inventory Order Calculator

A Python application built with Tkinter to manage and calculate restocking needs for inventory based on daily usage and sales data.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The **Inventory Order Calculator** helps streamline inventory management by allowing users to track current stock levels, calculate daily usage, and determine recommended restocking quantities based on historical usage data. This project is designed to provide a straightforward interface for quick calculations and inventory insights.

## Features

- **Input Fields** for current inventory, usage per thousand units, and daily sales.
- **Calculations** for daily usage and days until inventory depletion.
- **Restock Recommendations** based on calculated needs.
- **User-Friendly Interface** built with Tkinter, allowing anyone to operate it without command-line interaction.

## Requirements

- **Python 3.7+**: Ensure Python is installed on your system.
- **Tkinter**: Tkinter comes pre-installed with Python. No additional installation should be required for the UI.

## Installation

1. **Clone this repository**:
   ```bash
   git clone https://github.com/your-username/inventory-order-calculator.git
   cd inventory-order-calculator
   ```

2. **Install dependencies**:
   - Tkinter is included in standard Python installations, but if needed, use:
     ```bash
     pip install tk
     ```

## Usage

1. **Run the Application**:
   - Execute the `main.py` script:
     ```bash
     python main.py
     ```

2. **Enter Inventory Data**:
   - Input the current inventory level, usage per thousand units, and daily sales in the respective fields.

3. **Calculate Restock**:
   - Click on **Calculate Restock** to view the daily usage, estimated days until depletion, and the recommended restocking amount.

4. **Review Recommendations**:
   - Follow the displayed recommendations to maintain optimal stock levels.

## Contributing

Contributions are welcome! If you’d like to contribute, please fork the repository and create a pull request with your changes.

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## License

This project is licensed under the MIT License.

---