# Brief Information
This is an OTP Verification System. This is a python project uses only **streamlit** as an external dependency. 

#### To Install Streamlit
> pip install streamlit

This process can be achieved while setting up project

#### To Setup Project
1. Create Virtual Environment
   * In Terminal opened in desired folder
     * ` python -m venv venv `
   * Activate environment
     * ` venv\Scripts\activate `
   * Verify environment
     * ` where python ` command will give python path, which it would be from **venv**
2. Install required packages mentioned in *requirements.txt*
   * `python -m pip install -r requirements.txt`

#### Run Project
`streamlit run streamlit_app.py`


#### Process
1. Enter email to send OTP
   * If Success, will receive OTP on *email* and a timer will start.
2. Enter recieved OTP to verify.
   * OTP need to enter within specific time.
   * Success, will say *OTP Verifird*
   * Fail, will be because of *Time out* or *wrong otp*