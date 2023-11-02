from pywinauto.application import Application

# Specify the path to the application executable
app_path = r'C:\Path\To\Your\Application.exe'

# Launch the application
app = Application().start(app_path)

# Wait for the application to load (adjust timeout as needed)
main_window = app.window(title='Your Application Title', class_name='YourClassName')
main_window.wait('exists ready', timeout=10)

# Access a specific element (e.g., a label)
element = main_window.child_window(title='Label Title', control_type='Text')

# Retrieve the text content of the element
element_text = element.get_value()

# Print or use the element_text as needed
print(f"Element Text: {element_text}")

# Close the application
app.kill()
