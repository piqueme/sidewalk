1. Did any of your answers to Milestone 1 change (particularly the Additional Questions, your idea for your site, or team members)? Write the numbers for the questions whose answers have changed, and their new answers.

  1. **User Research**
	  2. Feature changes:
	  *	We removed the verification process, and replaced it with simply uploading a photo for each challenge in your completed quest. There's no longer a validation process for marking quests as completed.
	  *	The dashboard now shows a "quest of the day", and ""current quests" and "recent quests". We removed "posted quests".
	  *	Users can now upload images for their user icons and quest icons, which are automatically resized.
	  *	We plan to add more social features such as friending, and messaging or profile comments, but that isn't implemented in our MVP. 

  2. **Site Design**
	  3. We revamped the design for our site to have a more fantasy/urban feel.

  3. **MVP**
	  1. We did not include the Quest View/Manage page in our MVP.

---------------------------------------

2. Which features are implemented. To what extent are they complete?

  *	**Login/Registration** : Most features are fully functional for registering and logging in, though we currently don't check for repeat users when registering, don't send a confirmation email, and there are no Terms and Conditions.
  *	**Dashboard** : The Dashboard page is complete in content, with the exception of the Trending Quests panel (which currently doesn't calculate trending quests, and simply shows a list of the quests in the database). The layout design for the Dash is tentative, and will likely be improved later.
  *	**User Profiles** : Profile pages contain most planned features and functionalities, including user information, user stats, and scrollable carousels for current quests and completed quests.
  *	**Quest Pages** : Currently, we don't check to see if a user is currently on a quest and display different buttons (Start Quest instead of Complete/Forfeit) accordingly, so it's impossible to actually start a quest. The design of the quest pages are complete, and they display the quest's content correctly. However, there's a database issue with alloting memory for photos of victory, so they don't display. 
  *	**Quest Creation** : Quests can be posted and the form includes tooltips with instructions. We're planning to use AJAX to update the post page so that it shows a message saying that your quest is successfully (or unsuccessfully) posted, instead of redirecting you to a dummy page. The design of the posting page is tentative and will probably be improved on later. The location field doesn't have an autocomplete for locations-- this may be added in later, or we might drop the feature.
  *	**Quest Completion** : Clicking the "Complete" button on a quest page will display a modal with a form for uploading photos of victory and comments.
  *	**Quest Search** : Quest Search is fully functional based on keywords in the username and quest name. The front-end design of the page is also mostly complete.
  *	**Icons** : Users can now upload images for their user icons and quest icons, and the images are resized automatically so that the largest dimension is shrunken down to a uniform size, and the other dimensions are filled in with a default color so that the final image thumbnail is square. 

---------------------------------------

3. Are there any features you wanted to include in your MVP from Milestone 1 that are not complete? If so, which are they?
  *		We wanted to include the Quest View/Manage page, but didn't have time for it. The functionality for starting a quest is also incomplete. 

4. What additional features do you wish to implement? How far along on those features are you?
  * 	(Assuming this question refers to features that aren't already described in our Milestone 1 or above answers) A friending feature, and some method of communication such as commenting on profiles or private messaging
  * 	A quest photobook visualization for user profiles, where personal photos of victory are displayed with details about each quest in popovers, that's sharable (viewable even if you're not logged in). We haven't begun working on these two features yet. 
  *		Account settings page for editing user info and uploading an icon, and a Help & FAQ page. We have the pages for these two features set up, and need to fill in content.  

5. What technologies are you using for the back-end? Include any frameworks if relevant.
  *		Django, SQLite (MySQL on production), memcached

6. What technologies are you using for the front-end? Include Javascript frameworks such as jQuery, templating frameworks such as Handlebars.js, and other client-side frameworks such as Ember.js or Backbone.js.
  *		Twitter Bootstrap, jQuery, jQuery UI, raty (a jQuery plugin for quest ratings)

7. What is the main browser you are targeting? Must be one of our supported browsers.
  *		Chrome

8. What implementation unknown / risks are you still facing? Consider this an exercise of imagination, not a test of confidence.
  *		We don't have much error handling in place, so our website could contain bugs we don't know about. There might also be security holes. Another issues is that there might not be enough time to finish all the features we intend to include.