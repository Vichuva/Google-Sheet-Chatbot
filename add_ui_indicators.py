# Add UI indicators for context memory features

with open('app/streamlit_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the response display section
old_section = '''            if response['success']:
                # Display explanation
                st.markdown(response['explanation'])
                
                # Store message with metadata using save_message
                save_message(
                    "assistant",
                    response['explanation'],
                    {
                        "plan": response['plan'],
                        "data": response['data'].to_dict() if hasattr(response['data'], 'to_dict') else None,
                        "schema_context": response['schema_context'],
                        "data_refreshed": response['data_refreshed']
                    }
                )
                
                # Show data refreshed notification
                if response['data_refreshed']:
                    st.info("🔄 Data was automatically refreshed before processing this query")'''

new_section = '''            if response['success']:
                # Display explanation
                st.markdown(response['explanation'])
                
                # Show context memory indicators
                if response.get('from_cache'):
                    st.success(f"⚡ **Instant Answer** - Retrieved from cache (similarity: {response.get('similarity', 0):.2%})")
                
                if response.get('was_followup') and response.get('resolved_question'):
                    with st.expander("🔍 Context Resolution"):
                        st.markdown(f"**Original Question:** {prompt}")
                        st.markdown(f"**Resolved Question:** {response['resolved_question']}")
                
                # Store message with metadata using save_message
                save_message(
                    "assistant",
                    response['explanation'],
                    {
                        "plan": response['plan'],
                        "data": response['data'].to_dict() if hasattr(response['data'], 'to_dict') else None,
                        "schema_context": response['schema_context'],
                        "data_refreshed": response['data_refreshed']
                    }
                )
                
                # Show data refreshed notification
                if response['data_refreshed']:
                    st.info("🔄 Data was automatically refreshed before processing this query")'''

content = content.replace(old_section, new_section)

with open('app/streamlit_app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Successfully added context memory UI indicators')
