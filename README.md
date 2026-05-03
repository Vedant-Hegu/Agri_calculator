***

# AgriCalc: Agricultural Calculation and Monitoring System

AgriCalc is a Python-based desktop application built using Tkinter that facilitates the management and analysis of agricultural data. The application serves as a comprehensive dashboard to estimate seed quantities, plan germination targets, evaluate growth under varying environmental controls, and monitor historical sensor data. It is constructed with a custom-designed graphical interface, eliminating the need for heavy external visualization dependencies.

### Key Features

*   **Seed Estimator:**
    *   Calculates the total number of seeds based on the aggregate weight of a batch.
    *   Utilizes predefined reference weights (measured in grams per 50 seeds) for specific crops: Pavta (Lima Bean), Matar (Green Pea), and Mung (Green Gram).
*   **Germination Planner:**
    *   Predicts expected plant viability based on pre-configured historical germination rates, such as an 84% success rate for Pavta.
    *   Calculates the required surplus of seeds a user must sow to achieve a specific target yield.
*   **Growth Comparison Analysis:**
    *   Compares crop germination performance across differing environmental conditions, such as "Soil Controlled" or "Humidity and Moisture Control," against a "No Control" baseline.
    *   Renders an interactive line graph to visualize these comparative growth metrics.
    *   Displays crop-specific analytical insights, detailing optimum parameter ranges (e.g., temperatures of 21°C to 23°C) required for maximum yield.
*   **Environmental Monitoring Log:**
    *   Visualizes time-stamped, historical sensor readings for Temperature, Humidity, and Soil Moisture.
    *   Computes overall statistical averages for the active monitoring dataset.
    *   Incorporates an automated alert system that flags abnormal readings, warning the user if recorded temperatures exceed 30°C or if soil moisture levels drop below 65.

### Technical Architecture

*   **Frontend User Interface:** The graphical interface is built utilizing a custom component library (`agri_ui_components.py`) developed directly on Tkinter's Canvas and Frame modules. It incorporates a dynamic gradient sidebar, rounded interactive buttons with state transitions, and stylized input fields.
*   **Data Visualization:** Rather than relying on external dependencies such as Matplotlib, the application utilizes a custom `SimpleGraph` class to plot data points natively on a Tkinter Canvas.
*   **Modular Backend Architecture:** All mathematical conversions, statistical calculations, and data structures (including crop weights, historical success rates, and sensor logs) are isolated within the `AgriBackend` class (`agri_backend.py`) for a clean separation of concerns.
