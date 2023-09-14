# Project Environment Setup

## Steps:

1. **Create a Virtual Environment**:

   ```bash
   python3 -m venv venv
   ```

2. **Activate the Virtual Environment**:

   ```bash
   source venv/bin/activate
   ```

3. **Backend Setup**:

   - Install Poetry:

     ```bash
     pip install poetry==1.4.2
     ```

   - Install Dependencies:

     ```bash
     poetry install
     ```

   - Set up Environment Variables (`.env.example` is present as a template for the needed variables):
     \_Ensure you have your environment variables set up in a file named `.env.localdev`.\_

   - Run the Backend:
     ```bash
     poetry run uvicorn main:app --reload --host 0.0.0.0 --log-level=debug
     ```

4. **Frontend Setup**:

   - Install Dependencies:

     ```bash
     yarn install
     ```

   - Start the Development Server:
     ```bash
     yarn run dev
     ```

## Potential Improvements:

### Frontend:

- **Statictyping/interfaces for API calls:** Ensuring that all data from and to the API has a predictable shape will improve the reliability of the frontend code.

- **Service class for API calls and base API layer:** This provides a centralized place for all API related operations, making the codebase cleaner and more maintainable.

- **Adding proper layouts and folder structures:** Organizing the frontend resources into logical folders can improve code maintainability and make it easier for new developers to understand the structure.

### Backend:

- **Lacking static typing:** Implementing static typing can catch potential bugs early in the development process and improve code quality.

- **Pedantic objects and JSON API spec responses in builders:** Ensuring the response shape and type can be crucial for frontend-backend compatibility and for adhering to certain API standards.

- **Background jobs to handle retries and rate limiting:** This will ensure that the backend can handle large amounts of traffic and requests without overloading the system.

- **Webhook service to capture updates from API:** This can be useful for real-time data syncing and capturing events triggered by other services.

- **Used requests instead of Method python package:** Switching to a more modern package or one that fits the use case better can improve performance and reliability.

- **Missing any form of testing:** Implementing unit, integration, and end-to-end tests ensures that the backend functions as expected and makes refactoring safer.

- **Proper naming of functions:** Naming functions clearly and consistently makes the codebase more readable and maintainable.

- **Increased data validation - payments require correct plaid ids for lookup against merchants:** Ensuring all data input is validated properly can prevent many potential issues down the line.
