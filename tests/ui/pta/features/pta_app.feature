Feature: PTA Application Functionalities

  Scenario: Verify PTA Application Login
    Given Login to PTA application with sample credentials.
    Then "Logged In Successfully" text is visible.
    And Logout from PTA application.
