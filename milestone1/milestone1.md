User Research
=========

1. What problem does your application address, and how does your application address it?

    1. Our application addresses the issue of people not having the motivation to explore many parts of their city, as well as the issue of them not knowing what there is to explore.
    
    2. We address the problem by crowdsourcing ideas for fun and interesting activities to do in the city, and providing a motivational social rewards system for participating in these activities.

2. What are the killer features of your application?
    1. Terminology
        1. **Quests**
            1. Fun and interesting urban activities. 
            2. Titled, have name of poster, and optionally description text.
            3. Contain individual challenges (tasks), with corresponding locations, that need to be executed for quest completion
            4. Have skill points that will be distributed to a user for completion
            5. Have a rating based on well-definedness of the quest, determined by crowdsourcing
            6. Have an icon indicating the flavor of the quest.
        2. **Verification** 
            1. The process of determining whether proof submitted by another user for completion of a quest is adequate. 
        3. **NPC Rating**
            1. A user rating based on the quest ratings of posted quests, and accuracy of verifications. It is a measure of reliability.
        4. **Skills**
            1. Statistics for each user based on parameters related to urban exploration. These are like character statistics in RPGs. 
        5. **Classes**
            1. Unlockable user states discovered through skill growth. They are meant to indicate the sort of urban explorer a user is, as well as serve as a fun rewards system.
        6. **Trophies**
            1. Unlockable rewards for using parts of the site in various amounts. These are meant to provide small, fun incentives to users.
    2. Features
        1. **Login/Registration**: Our website is meant to provide a user-dependent service, and so needs these features. They will be implemented to provide the same sort of user experience as Facebook. 
        
        2. **Dashboard**: Users will have a default page upon logging in which has tools for quick access to many of the site’s other features, including digestible views of created quests, currently undertaken quests, and trending quests, the first two being prioritized by recency and the last being prioritized by a popularity metric. Through these views simple actions will also be made available, such as stopping of quests, and removal of posted quests.
        
        3. **User Profiles**: For each user, we have a “profile” model which gets its own page as a view. The model consists of the user’s name, the user’s stats, an optional profile picture, and the city they select as their residence. Users are able to access the page for their and other users’ profile pages depending on whether they are marked as private or public. The user will also have classes they have unlocked, and depending on one they have selected, the “theme”, or look and feel of their profile will be changed. Lastly, users will also be able to see a list of profiles’ corresponding users’ trophies on their profile pages.
        
        4. **Quest Pages**: Each quest created also will get its own quest page containing the quest information (name, list of challenges with locations, skill point distribution,…). In addition, on these pages, users will be able to accept/stop the quest, indicate completion and upload verification photos, and rate the quest. The quest page will also contain verification photos from anonymous users who have finished the quest.
        
        5. **Quest Creation**: Users can create quests, which are composed of the information provided earlier, resulting in the storage of their information in the database and the allowance of access to them by other features. They do this by using a form-like view to input the quest information, with things like location for challenges being required and constrained by places known to the system, and icons being selected by the user from a library of our standard icons.
        
        6. **Quest Search**: Users can lookup quests by name of poster or quest title using a standard search/autocomplete feature. Results will be displayed in a table of size fitting the screen, and will be scrollable. They can also filter the results by main skill they correspond to, as well as order the results by standard metrics, such as recency, popularity, and total skill point distribution.
        
        7. **Quest Viewing**: Users can look at the quests they are currently working on, see their challenges plotted on a map so that they have an idea of where they’re going to do what, and plan out efficient questing. Some mode of hard selection for quests in the view for this feature should send the user to the corresponding quest page, and soft selection should draw routes on the map between all of the locations for the challenges of that quest. The user will also be able to toggle whether completed and/or current quests are viewable.
        
        8. **Verification**: Users can anonymously and unbiasedly verify whether other users have completed quests through a verification system, by looking at pictures of random questors’ submitted quest proof along with quest information, and judging if the pictures indicate completion of the quest or not.  
        
        9. **Rewards**: For completing certain amounts of quests or certain types of quests, or even working on verification and posting quests, users will have trophies indicating their feats associated with their accounts, and will be notified of this. Similarly, unlockable classes will be distributed. 

3. Identify and briefly describe your target demographic. Who do you envision using your site?
    1. Pretty much anyone with the means to get around a city. This isn’t even being vague. But maybe more specifically, people who have at least a semblance of an urge to explore their city and/or want ideas for what to do in their city.
    
    2. Another user group consists of those people who are knowledgeable about their city and would like to share their wisdom.

4. Develop at least one use case for your site. This should be a list or table demonstrating a sequence of user actions and website responses that occur when a user attempts to complete a core task on your site. Make sure to indicate the task the user is trying to view/complete.
    1. Suppose Bob has just eaten at Yume wo Katare and would like to share his love of ramen with the world. He decides to upload a quest that contains a challenge for other users to eat at his new favorite restaurant.
    
        1. **User Action 1**: Go to site
           **Site Response 1**: Display home (login/signup) page.

        2. **User Action 2**: Enter login information in text boxes (username “mynameisbob”, pass “whee”).
           **Site Response 2**: Redirect to dashboard.
           
        3. **User Action 3**: Click on "Quest" on the navigation bar.
           **Site Response 3**: Display dropdown quest menu.
           
        4. **User Action 4**: Click on “Post Quest” button.
           **Site Response 4**: Redirect to “Post Quest” page.
           
        5. **User Action 5**: Input quest name (“Ramen All Night”), description (“Eat the best ramen ever at Yume wo Katare”), skill point distribution and only challenge name (“Eat ramen”) into corresponding text fields.
           **Site Response 5**: Update view with text, move cursor to first challenge location.
           
        6. **User Action 6**: Input (“Yume wo Katare”), select appropriate address from autocomplete.
           **Site Response 6**: Update view with text.
           
        7. **User Action 7**: Click “Done” button.
           **Site Response 7**: Popup “Submitted yay!”
            
----------

Site Design
========
Think hard about your most complicated page. What are the important features of this page? What usability problems may come up? For your most important page:

1. Draw out, by hand, three different designs for this page. Scan these for your submission.

2. Make a list of 3 pros and 3 cons for each design.

    ![Sketches](http://github.mit.edu/mit6470/nothomies/raw/master/sketches.png)

3. Pick the best design and mock it up using an image editing program (i.e. Photoshop or Gimp) or using HTML/CSS. Submit a screenshot of this mockup.

    ![Mockup](http://github.mit.edu/mit6470/nothomies/raw/master/mockup.png) 

----------

Minimal Viable Product
========

Please answer the following questions about your plan for your MVP:

1. What features do you plan to implement? How critical are they to the proper functioning of your application?
    1. **Login/ Registration**
        1. All features implemented.
        2. We feel that all features described as part of login and registration are necessary, since we need to keep a track of the people using our application in order to help them know long-term what they are looking for in their city, and planning how to do the activities they find. In addition, we must track user information in order to give them our incentives!
    2. **Dashboard**
        1. Quick viewing of current quests and posted quests implemented.
        2. The features listed, according to us, are critical to the function of the website, since the powerful features we’ve listed for working with quests in the other parts of the site can take time to work with, and most users will find much greater efficiency in a quickly digestible view which takes advantage of the relevance of the recency in their activities.
    3. **User Profiles**
        1. Pages displaying information on name, location, their stats, and their optional profile image will be implemented. Privately viewable, lists of completed/current quests will also be impleneted.
        2. Users will be able to visit other user’s profiles, so long as they are public.
        3. The user profile feature, with the components listed here, are also critical to the application from our perspective, as it is necessary for users to be able to view their personal information according to the service, and both ensure its correctness, as well as appreciate what they have personally done with the service (through their stats, and lists of completed/current quests, etc.). 
    4. **Quest Pages**
        1. Pages for each quest with the identifying information for the quest, including name, description, skill point crediting, and list of challenges with locations, will be implemented. 
        2. Buttons for acceptance and stopping of quests, as well as completion submission will also be implemented.
        3. These features are all considered necessary since quests are the center of the site’s attention - users need to be able to access information about quests easily and have their own actions relative to each quest easily accessible as well.
    5. **Quest Creation**
        1. All features implemented.
        2. Name, description, challenges (tasks), stat point crediting and a communicative icon are all essential to the understanding of a quest; since the site revolves around taking quests and executing them, it then follows that easily creating quests with all these components is required.
    6. **Quest Search**
        1. Table for displaying quest listings with search/autocomplete by quest name or poster name will be implemented.
        2. We feel that users need to be able to lookup quests with a search/autocomplete feature to find what sort of quests they’re looking for quickly and efficiently while maintaining an economic view, so these are critical features. Were these sorts of features not present, users would only be able to access quests via their dashboard, a summarized view which is meant to help find only trending quests, or by going to other users’ profiles and looking at the quests they may have completed, a very inefficient procedure. 
    7. **Quest Viewing**
        1. Listing of current quests, along with the side map view will be implemented.
        2. Forwarding to quest pages on hard selection of quest listings will be implemented.
        3. These features too are critical to our site’s function. Users should have some way of efficiently and effectively reminding themselves of what they’re planning to do, and see how they might go about getting to the places for their questing efficiently. To do that, they need these features. 
    8. **Verification**
        1. All features implemented.
        2. These feature too are essential, as we need a way of ensuring that people are actually doing quests to get credit for them in the system, and we don’t know how to do this effectively without crowdsourcing. 

2. What features do you plan to leave out? How critical are they to the proper functioning of your application?
    1. **Dashboard** 
        1. The view of a user’s “trending” quests (most popular/highest rated) will be left out. 
        2. This feature is not critical to the app in that users will still be able to complete and navigate their quests, although having the “trending” row may allow users to do so more easily.
    2. **User Profiles**
        1. The user profile will be missing the customizable theme, the class of the user, and the user’s list of trophies. 
        2. These are merely for the user’s enjoyment, and while they may have some impact on the friendliness of our site, the site could plausibly function without them.
    3. **Quest Pages**
        1. Individual quest pages will be missing the horizontally scrollable row that contains the verification photos of other users that have completed the quest. 
        2. Again, this is mostly for user experience, and not necessary for function of the system.
    4. **Quest Search**
        1. We will not be implementing the filters or ordering (filter by skill points, order by chronology, rating, and popularity) options. 
        2. These features are not necessary for usage of the application, but including them will definitely improve user experience.
    5. **Quest View**
        1. Our MVP will not contain the feature that shows the quest route on the map when a specific quest is single clicked or the feature that allows users to toggle between current and completed quests. 
        2. These features are nice to have for users, because it allows them visualize their route, but it by no means is crucial.

3. Are there any other aspects of your application that are reduced in your MVP? Examples including limited fake datasets, stylistic concerns, security concerns, etc.
    1. Our application will have a reduced library of icons for users to choose from for their quest icons.
    2. Several fake users and fake quests will be created to populate the database.
        

-------------------

Additional Questions
========
Please answer the following questions. Please be succinct as possible.

1. Who is in your team? You may list at most 3 people (4 if you are not competing in the main division). For each member list the full legal name, .edu e-mail, school, major(s), year, and graduate/undergraduate status. For each team member, also indicate whether they are registered to take the class for credit.
    1. Anying Li, anyingl@mit.edu, MIT, Course 6, 2016, undergrad
    2. Dongfang Mi, tianm@mit.edu, MIT, Course 6, 2016, undergrad
    3. Sumit Gogia, summit@mit.edu, MIT, Course 6, 2015, undergrad

2. Which of the themes does your application match best? Be as brief as you can.
    1. Our application is most closely related to Urban Living, Exploration, and Transportation.

3. What technology do you plan to use for your server-side programming (e.g. PHP, Ruby on Rails, etc)?
    1. We’re planning to use Python/Django with SQLite.

4. What risks do you envision preventing you from successfully implementing your idea? Consider this an exercise of imagination, not a test of confidence.
    1. We imagine many many opportunities for failure, but far more for success! Some of the possible issues which we are sure to overcome include an abundance of features that we may not have the manpower to implement in time, our “lack” of understanding of security resulting in the downfall of our website, and problems with libraries that we are “unfamiliar” with but seem to expect to use instantaneously. In short, we are “scared” of overambition - but a little fear in exploration is always a good thing!

5. Are you planning to participate in the competition? If so, are you competing in the main division or the rookie division? Your answer will solely be used for planning purposes.
    1. Yes, we are planning to participate in the main division.
