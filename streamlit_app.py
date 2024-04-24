import time
import streamlit as st
import functionality as f
from timeit import default_timer as timer


def main():

    st.title("OTP Verification")
    start_time=timer()

    if 'send_mail_flag' not in st.session_state:
        st.session_state.send_mail_flag=False
    if 'generated_otp' not in st.session_state:
        st.session_state['generated_otp']=0
    if 'verify_otp_form' not in st.session_state:
        st.session_state.verify_otp_form=False
    if 'time_in_sec' not in st.session_state:
        st.session_state.time_in_sec=1*60
    if 'start_time' not in st.session_state:
        st.session_state.start_time=start_time
    if 'initialvalue' not in st.session_state:
        st.session_state.initialvalue=None
        

    with st.form('send_otp_form'):
        email_string=st.text_input(label="Enter Email To Send OTP", placeholder="username@domain")
        submitted=st.form_submit_button("Send OTP")
        otp_msg_placeholder=st.empty()
        if submitted:
            st.session_state.send_mail_flag, email_string = f.validate_email(email_string, otp_msg_placeholder)
            st.session_state.verify_otp_form=False


    if st.session_state.send_mail_flag:
        st.session_state.generated_otp=f.send_mail(email_string, otp_msg_placeholder)
        if st.session_state.generated_otp!=0:
            st.session_state.send_mail_flag=False
            st.session_state.verify_otp_form=True


    if st.session_state.verify_otp_form==True:
        with st.form('my_form'):
            name=st.text_input(label="Enter Received OTP")
            submitted=st.form_submit_button("Verify")
            verify_msg_placeholder=st.empty()

            if submitted:
                received_otp=int(name.title())
                if received_otp==st.session_state.generated_otp:
                    verify_msg_placeholder.info("OTP Verified")
                    st.session_state.verify_otp_form=False
                    time.sleep(2)
                    st.rerun()
                else:
                    time.sleep(1)
                    end_time=timer()
                    st.session_state.time_in_sec = st.session_state.time_in_sec - int(end_time-st.session_state.start_time)
                    verify_msg_placeholder.info("Incorrect OTP")
                    st.session_state.start_time=timer()
                    f.streamlit_count_down(st.session_state.time_in_sec)
                    st.session_state.verify_otp_form=False
                    verify_msg_placeholder.info("Time Expired")
                    time.sleep(2)
                    st.rerun()
                    
            else:
                st.session_state.start_time=timer()
                f.streamlit_count_down(st.session_state.time_in_sec)
                st.session_state.verify_otp_form=False
                verify_msg_placeholder.text("Time Expired")
                time.sleep(2)
                st.rerun()


if __name__ == '__main__':
    main()