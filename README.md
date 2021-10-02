# ifa-tcf-catcher
Catches Rendez-Vous for TCF Tests (DAP, SO, CANADA) by automating requests to https://portail.if-algerie.com


# How to Run
## Preparation

Use Some IDE to Edit the main file.

Fill the variables with your IFA account's cookies and the TCF Type that you want **(TCF DAP, TCF SO, TCF CANADA)**.

### Cookies

Once you login with your own account in your browser -like Chrome- :

1. Inspect Element
2. Open the Network tab
3. Refresh the page with F5 or Ctrl+R
4. When new requests appear, go to the first one and select it
5. Go to Requests Headers
6. Copy your cookies and pass them into the main python file -in the cookies variable-

### X-CSRF-TOKEN

1. After copying cookies, return back to Elements.
2. Ctrl+F to search the html code of the page.
3. Look for "csrf-token"
4. You will find a \<meta\> tag whose 'name' attribute is "csrf-token"
5. The X-CSRF-TOKEN is the "content" attribute's value.
6. Copy the value to the script in the "X-CSRF-TOKEN" keyword of the x dictionary.

## Execution

**Method 1 :** Simply click on the main file.

**Method 2 :** Excecute the command `python __init__.py` from Terminal (for UNIX Systems) or from cmd/PowerShell (Windows)

# Python Libraries

- Requests `pip install requests`
