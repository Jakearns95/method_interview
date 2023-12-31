# Project Environment Setup

[Example Video](https://drive.google.com/file/d/1sierqqyTTh-aZi7sJLQ6Kuw1saCspacP/view?usp=sharing)

## Steps:

1. **Create a Virtual Environment**:

   - ensure you have python 3.9 installed

   ```bash
   python3 -m venv venv
   ```

2. **Activate the Virtual Environment**:

   ```bash
   source venv/bin/activate
   ```

3. **Backend Setup**:

   - Navigate to `/backend`

   - Install Poetry:

     ```bash
     pip install poetry==1.4.2
     ```

   - Install Dependencies:

     ```bash
     poetry install
     ```

   - Set up Environment Variables (`.env.example` is present as a template for the needed variables):

     - Ensure you have your environment variables set up in a file named `.env.localdev`.

   - Run the Backend:
     ```bash
     poetry run uvicorn main:app --reload --host 0.0.0.0 --log-level=debug
     ```

4. **Frontend Setup**:

   Use [nvm](https://github.com/nvm-sh/nvm#installing-and-updating) to manage node versions. The version is set in the `.nvmrc` file so you only need to run the following commands:

   ```
   nvm install
   nvm use
   ```

   To test a specific version use the following:

   ```
   nvm install 18.12.1
   nvm use 18.12.1
   ```

   Install Yarn as the Node package manager (note: don't install packages using `npm`)

   ```
   npm install --global yarn
   ```

   - Navigate to `/frontend`

   - Install Dependencies:

     ```bash
     yarn install
     ```

   - Start the Development Server:
     ```bash
     yarn run dev
     ```

## Potential Improvements:

## Frontend:

- **Static Typing and Interfaces for API Calls**:

  - Introduce static typing and interfaces to make sure data interacting with the API is consistent. This enhances the frontend's robustness.

- **Service Class for API Calls & Base API Layer**:

  - Centralize all API operations within a dedicated service class, streamlining the code and simplifying maintenance.

- **Structured Layouts and Folder Organization**:
  - Strategically structure frontend assets in intuitive folders. This fosters better maintainability and aids newcomers in navigating the codebase.

## Backend:

- **Static Typing**:

  - Adopt static typing to preemptively detect bugs, elevating code quality.

- **Pydantic Objects & JSON API Spec in Builders**:

  - Standardize response formats to ensure harmony between the frontend and backend, and to align with API best practices.

- **Background Job Management**:

  - Introduce background jobs for retry mechanisms and rate limiting. This ensures efficient handling of traffic surges without system overload.

- **Webhook Services for API Updates**:

  - Implement webhooks to seamlessly synchronize real-time data and capture events instigated by external services.

- **Optimal Package Usage**:

  - Consider transitioning from 'requests' to the 'Method' python package or another modern alternative for better performance and reliability.

- **Testing**:

  - Introduce diverse testing layers (unit, integration, end-to-end) to verify backend operations, ensuring functionality and facilitating safer code refactoring.

- **Function Naming Convention**:

  - Opt for clear and consistent function names to enhance code readability and maintainability.

- **Rigorous Data Validation**:
  - Strengthen data validation processes, especially for payments, to ensure the accuracy of Plaid IDs when cross-referencing with merchants.
