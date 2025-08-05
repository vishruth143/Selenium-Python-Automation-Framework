Feature: PTA Application Functionalities

  Scenario: Successful login and logout from the PTA application
    Given the user navigates to the PTA application home page
    When  the user clicks on the 'PRACTICE' link
    And   the user clicks on the 'Test Login Page' link
    And   the user login to PTA application with valid credentials
    Then  the user should see a 'Logged In Successfully' message
    And   the user logs out from the PTA application
