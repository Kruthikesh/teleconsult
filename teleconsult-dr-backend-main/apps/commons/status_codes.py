# Common Status Codes


class CommonStatusCodes:
    SERVER_EXCEPTION = {
        'code': 500, 'reason': 'Internal Server exception, please find exception details for more info'
    }


# App auth status codes
class AppAuthStatusCodes:
    USER_FOUND = {
        'code': 200, 'reason': 'User found'
    }
    USER_NOT_FOUND = {
        'code': 1002, 'reason': 'User not found due to incorrect email or password'
    }
    INCORRECT_CREDS = {
        'code': 1003, 'reason': 'Incorrect email/password. Please register if not an existing user!'
    }
    MISSING_FIELDS_FOR_LOGIN = {
        'code': 1004, 'reason': 'Either email or password is missing'
    }
    MISSING_FIELDS_FOR_RESET = {
        'code': 1005, 'reason': 'Please enter a valid email'
    }
    LOGIN_FAILED = {
        'code': 1006, 'reason': 'Error, Unable to login!'
    }
    FB_USER_ID_ALREADY_LINKED = {
        'code': 1007, 'reason': 'Error, Unable to login! The facebook account is already linked to an another user.'
    }
    GOOGLE_USER_ID_ALREADY_LINKED = {
        'code': 1008, 'reason': 'Error, Unable to login! The google account is already linked to an another user.'
    }
    COULD_NOT_SIGNUP_FROM_FB = {
        'code': 1007, 'reason': 'Profile not found and hence sign-up is not complete. Retry again'
    }


# customer status codes
class UserStatusCodes:
    REGISTRATION_SUCCESS = {
        'code': 200, 'reason': 'Yaaay! You have successfully created your account. '
                               'Please login using your credentials to continue.'
    }
    USER_DETAILS_OBTAINED = {
        'code': 200, 'reason': 'User details obtained'
    }
    USER_LOGGED_OUT = {
        'code': 200, 'reason': 'User logged out successfully'
    }
    PASSWORD_CHANGED = {
        'code': 200, 'reason': 'Password changed successfully'
    }
    PROFILE_DETAILS = {
        'code': 200, 'reason': 'Profile details found'
    }
    EMAIL_VERIFICATION_LINK_SENT = {
        'code': 200, 'reason': 'Verification email successfully sent'
    }
    NEW_PASSWORD_SENT_TO_EMAIL = {
        'code': 200, 'reason': 'An email with a new password has been sent to your registered email id.'
    }
    REGISTRATION_FAILED = {
        'code': 2002, 'reason': 'Registration failed'
    }
    MISSING_FIELDS_FOR_REGISTRATION = {
        'code': 2003, 'reason': 'Missing mandatory fields for sign-up'
    }
    INVALID_USER_TYPE = {
        'code': 2004, 'reason': 'Invalid user type'
    }
    SAME_USER_EXISTS = {
        'code': 2005, 'reason': 'User already exists'
    }
    LOGIN_FAILED = {
        'code': 2006, 'reason': 'Login failed'
    }
    USER_NOT_FOUND = {
        'code': 2007, 'reason': 'User not found'
    }
    NEW_PASSWORD_NOT_FOUND = {
        'code': 2008, 'reason': 'Please enter a valid password'
    }
    EMAIL_NOT_VERIFIED = {
        'code': 2009, 'reason': 'Email not verified, please verify your email.'
    }
    EMAIL_VERIFIED = {
        'code': 200, 'reason': 'Email verified successfully.'
    }
    EMAIL_VERIFICATION_FAILED = {
        'code': 2010, 'reason': 'Error, Email verification failed.'
    }
    LOGIN_FAILED_IN_GOOGLE_SSO = {
        'code': 2011, 'reason': 'Error, Something went wrong while fetching the details from google.'

    }
    LOGIN_FAILED_IN_FB_SSO = {
        'code': 2012, 'reason': 'Error, Something went wrong while fetching the details from facebook.'
    }
    USER_NOT_ACTIVE = {
        'code': 2013, 'reason': 'Sorry!! your account has been disabled. Please contact administrator.'
    }
    OTP_SENT = {
        'code': 200,
        'reason': 'We have sent you an passcode to your phone number. Please confirm to verify your phone number.'
    }
    OTP_VERIFIED = {
        'code': 200, 'reason': 'Your phone number is successfully verified.'
    }
    PHONE_NUMBER_NOT_FOUND = {
        'code': 2014, 'reason': 'Phone number not found.'
    }
    MISSING_OTP = {
        'code': 2015,
        'reason': 'Missing passcode'
    }
    INVALID_OTP = {
        'code': 2016,
        'reason': 'Invalid OTP.'
    }


class PatientStatusCodes:
    PATIENT_PROBLEM_FOUND = {
        'code': 200,
        'reason': 'Patient problem found'
    }
    PATIENT_ALL_PROBLEMS_FOUND = {
        'code': 200,
        'reason': 'Patient all problem found'
    }
    PATIENT_PROBLEM_NOT_FOUND = {
        'code': 3001,
        'reason': 'Patient problem not found'
    }
    PATIENT_PROBLEM_UPLOADED = {
        'code': 200,
        'reason': 'Patient problem uploaded'
    }
    PATIENT_NOT_FOUND = {
        'code': 3002,
        'reason': 'Patient not found'
    }


class PatientProblemStatusCodes:
    MISSING_FIELDS_FOR_PROBLEM_EXPLANATION = {
        'code': 4001, 'reason': 'Missing mandatory fields for problem explanation. '
                                'Make sure you have entered problem description and expectations'
    }
    PROBLEM_EXPLANATION_NOT_FOUND = {
        'code': 4002, 'reason': 'Details not found. Invalid problem explanation id.'
    }
    PROBLEM_EXPLANATION_FOUND = {
        'code': 200, 'reason': 'Problem explanation found'
    }
    REVIEWS_BY_PATIENT_NOT_FOUND = {
        'code': 4003, 'reason': 'No reviews given by patient'
    }

class DoctorStatusCodes:
    DOCTOR_RESPONSE_UPLOADED = {
        'code': 200,
        'reason': 'Doctor response uploaded'
    }
    DOCTOR_RESPONSE_FOUND = {
        'code': 200,
        'reason': 'Doctor response found'
    }
    NO_DOCTOR_RESPONSE = {
        'code': 200,
        'reason': 'No doctor response'
    }
    DOCTOR_RESPONSE_FETCH_FAILED = {
        'code': 5001,
        'reason': 'Could not fetch doctor response'
    }
    DOCTOR_NOT_FOUND = {
        'code': 5002,
        'reason': 'Doctor not found'
    }
    


class TCDStatusCodes:
    MISSING_PATIENT_OR_TCD_DETAILS = {
        'code': 6001,
        'reason': 'Missing patient/tcd information'
    }
    TCD_FOUND = {
        'code': 200, 'reason': 'TCD found'
    }
    TCD_NOT_FOUND = {
        'code': 200, 'reason': 'TCD not found. Invalid id'
    }
    MISSING_FIELDS_FOR_FEEDBACK = {
        'code': 200, 'reason': 'Invalid inputs'
    }
    TCD_FEEDBACK_UPDATED = {
        'code': 200, 'reason': 'Feedback saved'
    }
    TCD_FEEDBACK_OBTAINED = {
        'code': 200, 'reason': 'TCD feedback obtained'
    }
    TCD_FEEDBACK_NOT_FOUND = {
        'code': 200, 'reason': 'TCD not found. Invalid id'
    }
