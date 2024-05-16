export function history() {
        // HISTORY STUFF
        /////////////////
        //-         const saveButton = document.getElementById('save');
        //-         const filenameInput = document.getElementById('save-name');
        //-         const saveConfirmButton = document.getElementById('save-confirm');
        //-
        //-         saveButton.addEventListener('click', function() {
        //-           filenameInput.classList.remove("d-none")
        //-           saveConfirmButton.classList.remove("d-none")
        //-           saveButton.classList.add("d-none")
        //-           filenameInput.focus();
        //-         });
        //-
        //-         function restoreSaveButton(){
        //-           filenameInput.classList.add("d-none")
        //-           saveConfirmButton.classList.add("d-none")
        //-           saveButton.classList.remove("d-none")
        //-         }

        // TODO will be converted to a htmx trigger
        //function saveHistory(){
        //-           const saveName = filenameInput.value.trim();
        //-           filenameInput.value = '';
        //-
        //-           // TODO ajax call replacing history
        //-           restoreSaveButton();
        //-         }
        //-
        //-
        //-         filenameInput.addEventListener('keydown', function(event) {
        //-           // TODO will be a htmx trigger
        //-           if (event.key === 'Enter') {
        //-             event.preventDefault(); // Prevent the default action to avoid form submission or any other unintended effects
        //-             saveHistory();
        //-           } else if (event.key === 'Escape') {
        //-             event.preventDefault(); // Prevent the default action to avoid form submission or any other unintended effects
        //-             restoreSaveButton();
        //-           }
        //-         });
        //filenameInput.addEventListener('blur', restoreSaveButton);
        // TODO will get a htmx event
        //saveConfirmButton.addEventListener('click', saveHistory);
}