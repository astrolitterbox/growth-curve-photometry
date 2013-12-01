


<!DOCTYPE html>
<html>
  <head prefix="og: http://ogp.me/ns# fb: http://ogp.me/ns/fb# githubog: http://ogp.me/ns/fb/githubog#">
    <meta charset='utf-8'>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <title>growth-curve-photometry/vimos/sdss/readGalfit.py at newProduction · astrolitterbox/growth-curve-photometry</title>
    <link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="GitHub" />
    <link rel="fluid-icon" href="https://github.com/fluidicon.png" title="GitHub" />
    <link rel="apple-touch-icon" sizes="57x57" href="/apple-touch-icon-114.png" />
    <link rel="apple-touch-icon" sizes="114x114" href="/apple-touch-icon-114.png" />
    <link rel="apple-touch-icon" sizes="72x72" href="/apple-touch-icon-144.png" />
    <link rel="apple-touch-icon" sizes="144x144" href="/apple-touch-icon-144.png" />
    <link rel="logo" type="image/svg" href="https://github-media-downloads.s3.amazonaws.com/github-logo.svg" />
    <meta property="og:image" content="https://github.global.ssl.fastly.net/images/modules/logos_page/Octocat.png">
    <meta name="hostname" content="github-fe128-cp1-prd.iad.github.net">
    <meta name="ruby" content="ruby 1.9.3p194-tcs-github-tcmalloc (e1c0c3f392) [x86_64-linux]">
    <link rel="assets" href="https://github.global.ssl.fastly.net/">
    <link rel="conduit-xhr" href="https://ghconduit.com:25035/">
    <link rel="xhr-socket" href="/_sockets" />
    


    <meta name="msapplication-TileImage" content="/windows-tile.png" />
    <meta name="msapplication-TileColor" content="#ffffff" />
    <meta name="selected-link" value="repo_source" data-pjax-transient />
    <meta content="collector.githubapp.com" name="octolytics-host" /><meta content="collector-cdn.github.com" name="octolytics-script-host" /><meta content="github" name="octolytics-app-id" /><meta content="5F5BF14C:263E:B31B834:529B19FA" name="octolytics-dimension-request_id" /><meta content="1590204" name="octolytics-actor-id" /><meta content="astrolitterbox" name="octolytics-actor-login" /><meta content="3999993443124889b3a04d98674d3a45d40fffe6591de672f24d56e69c668236" name="octolytics-actor-hash" />
    

    
    
    <link rel="icon" type="image/x-icon" href="/favicon.ico" />

    <meta content="authenticity_token" name="csrf-param" />
<meta content="zLxAz81l0NOJ0PF6q68TRcyEIcMRBkTFmoXgF8jguBE=" name="csrf-token" />

    <link href="https://github.global.ssl.fastly.net/assets/github-0f5611c27a5a2a6928dc6e99d63581265b963e34.css" media="all" rel="stylesheet" type="text/css" />
    <link href="https://github.global.ssl.fastly.net/assets/github2-6102d7944435d804d870f38bf20f1e16fe40a4d0.css" media="all" rel="stylesheet" type="text/css" />
    

    

      <script src="https://github.global.ssl.fastly.net/assets/frameworks-f78f9db32da9343ba16e477c7b54aa5b971fecbd.js" type="text/javascript"></script>
      <script src="https://github.global.ssl.fastly.net/assets/github-0027dfa2fe63e83319cafa77f57322ac81018255.js" type="text/javascript"></script>
      
      <meta http-equiv="x-pjax-version" content="0741c61298bb1b3e07c83e272155021d">

        <link data-pjax-transient rel='permalink' href='/astrolitterbox/growth-curve-photometry/blob/78863ca9fa87dd3be7f06e74aca2d817a0171f5a/vimos/sdss/readGalfit.py'>
  <meta property="og:title" content="growth-curve-photometry"/>
  <meta property="og:type" content="githubog:gitrepository"/>
  <meta property="og:url" content="https://github.com/astrolitterbox/growth-curve-photometry"/>
  <meta property="og:image" content="https://github.global.ssl.fastly.net/images/gravatars/gravatar-user-420.png"/>
  <meta property="og:site_name" content="GitHub"/>
  <meta property="og:description" content="growth-curve-photometry - some bad research code for growth curve photometry and analysis of galaxies"/>

  <meta name="description" content="growth-curve-photometry - some bad research code for growth curve photometry and analysis of galaxies" />

  <meta content="1590204" name="octolytics-dimension-user_id" /><meta content="astrolitterbox" name="octolytics-dimension-user_login" /><meta content="3900736" name="octolytics-dimension-repository_id" /><meta content="astrolitterbox/growth-curve-photometry" name="octolytics-dimension-repository_nwo" /><meta content="true" name="octolytics-dimension-repository_public" /><meta content="false" name="octolytics-dimension-repository_is_fork" /><meta content="3900736" name="octolytics-dimension-repository_network_root_id" /><meta content="astrolitterbox/growth-curve-photometry" name="octolytics-dimension-repository_network_root_nwo" />
  <link href="https://github.com/astrolitterbox/growth-curve-photometry/commits/newProduction.atom" rel="alternate" title="Recent Commits to growth-curve-photometry:newProduction" type="application/atom+xml" />

  </head>


  <body class="logged_in  env-production linux vis-public page-blob">
    <div class="wrapper">
      
      
      
      


      <div class="header header-logged-in true">
  <div class="container clearfix">

    <a class="header-logo-invertocat" href="https://github.com/">
  <span class="mega-octicon octicon-mark-github"></span>
</a>

    
    <a href="/notifications" class="notification-indicator tooltipped downwards" data-gotokey="n" title="You have unread notifications">
        <span class="mail-status unread"></span>
</a>

      <div class="command-bar js-command-bar  in-repository">
          <form accept-charset="UTF-8" action="/search" class="command-bar-form" id="top_search_form" method="get">

<input type="text" data-hotkey=" s" name="q" id="js-command-bar-field" placeholder="Search or type a command" tabindex="1" autocapitalize="off"
    
    data-username="astrolitterbox"
      data-repo="astrolitterbox/growth-curve-photometry"
      data-branch="newProduction"
      data-sha="209c05b2be2d342c8e5b64fca42f3a45ebda8e35"
  >

    <input type="hidden" name="nwo" value="astrolitterbox/growth-curve-photometry" />

    <div class="select-menu js-menu-container js-select-menu search-context-select-menu">
      <span class="minibutton select-menu-button js-menu-target">
        <span class="js-select-button">This repository</span>
      </span>

      <div class="select-menu-modal-holder js-menu-content js-navigation-container">
        <div class="select-menu-modal">

          <div class="select-menu-item js-navigation-item js-this-repository-navigation-item selected">
            <span class="select-menu-item-icon octicon octicon-check"></span>
            <input type="radio" class="js-search-this-repository" name="search_target" value="repository" checked="checked" />
            <div class="select-menu-item-text js-select-button-text">This repository</div>
          </div> <!-- /.select-menu-item -->

          <div class="select-menu-item js-navigation-item js-all-repositories-navigation-item">
            <span class="select-menu-item-icon octicon octicon-check"></span>
            <input type="radio" name="search_target" value="global" />
            <div class="select-menu-item-text js-select-button-text">All repositories</div>
          </div> <!-- /.select-menu-item -->

        </div>
      </div>
    </div>

  <span class="octicon help tooltipped downwards" title="Show command bar help">
    <span class="octicon octicon-question"></span>
  </span>


  <input type="hidden" name="ref" value="cmdform">

</form>
        <ul class="top-nav">
          <li class="explore"><a href="/explore">Explore</a></li>
            <li><a href="https://gist.github.com">Gist</a></li>
            <li><a href="/blog">Blog</a></li>
          <li><a href="https://help.github.com">Help</a></li>
        </ul>
      </div>

    


  <ul id="user-links">
    <li>
      <a href="/astrolitterbox" class="name">
        <img height="20" src="https://1.gravatar.com/avatar/1d7d4e23d2c4a56b10f8439c0b1e2c73?d=https%3A%2F%2Fidenticons.github.com%2Fd8296e571d7b0aa37c8bbb30ecc8747a.png&amp;r=x&amp;s=140" width="20" /> astrolitterbox
      </a>
    </li>

      <li>
        <a href="/new" id="new_repo" class="tooltipped downwards" title="Create a new repo" aria-label="Create a new repo">
          <span class="octicon octicon-repo-create"></span>
        </a>
      </li>

      <li>
        <a href="/settings/profile" id="account_settings"
          class="tooltipped downwards"
          aria-label="Account settings "
          title="Account settings ">
          <span class="octicon octicon-tools"></span>
        </a>
      </li>
      <li>
        <a class="tooltipped downwards" href="/logout" data-method="post" id="logout" title="Sign out" aria-label="Sign out">
          <span class="octicon octicon-log-out"></span>
        </a>
      </li>

  </ul>

<div class="js-new-dropdown-contents hidden">
  

<ul class="dropdown-menu">
  <li>
    <a href="/new"><span class="octicon octicon-repo-create"></span> New repository</a>
  </li>
  <li>
    <a href="/organizations/new"><span class="octicon octicon-organization"></span> New organization</a>
  </li>



    <li class="section-title">
      <span title="astrolitterbox/growth-curve-photometry">This repository</span>
    </li>
      <li>
        <a href="/astrolitterbox/growth-curve-photometry/issues/new"><span class="octicon octicon-issue-opened"></span> New issue</a>
      </li>
      <li>
        <a href="/astrolitterbox/growth-curve-photometry/settings/collaboration"><span class="octicon octicon-person-add"></span> New collaborator</a>
      </li>
</ul>

</div>


    
  </div>
</div>

      

      




          <div class="site" itemscope itemtype="http://schema.org/WebPage">
    
    <div class="pagehead repohead instapaper_ignore readability-menu">
      <div class="container">
        

<ul class="pagehead-actions">

    <li class="subscription">
      <form accept-charset="UTF-8" action="/notifications/subscribe" class="js-social-container" data-autosubmit="true" data-remote="true" method="post"><div style="margin:0;padding:0;display:inline"><input name="authenticity_token" type="hidden" value="zLxAz81l0NOJ0PF6q68TRcyEIcMRBkTFmoXgF8jguBE=" /></div>  <input id="repository_id" name="repository_id" type="hidden" value="3900736" />

    <div class="select-menu js-menu-container js-select-menu">
      <a class="social-count js-social-count" href="/astrolitterbox/growth-curve-photometry/watchers">
        2
      </a>
      <span class="minibutton select-menu-button with-count js-menu-target" role="button" tabindex="0">
        <span class="js-select-button">
          <span class="octicon octicon-eye-unwatch"></span>
          Unwatch
        </span>
      </span>

      <div class="select-menu-modal-holder">
        <div class="select-menu-modal subscription-menu-modal js-menu-content">
          <div class="select-menu-header">
            <span class="select-menu-title">Notification status</span>
            <span class="octicon octicon-remove-close js-menu-close"></span>
          </div> <!-- /.select-menu-header -->

          <div class="select-menu-list js-navigation-container" role="menu">

            <div class="select-menu-item js-navigation-item " role="menuitem" tabindex="0">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <div class="select-menu-item-text">
                <input id="do_included" name="do" type="radio" value="included" />
                <h4>Not watching</h4>
                <span class="description">You only receive notifications for conversations in which you participate or are @mentioned.</span>
                <span class="js-select-button-text hidden-select-button-text">
                  <span class="octicon octicon-eye-watch"></span>
                  Watch
                </span>
              </div>
            </div> <!-- /.select-menu-item -->

            <div class="select-menu-item js-navigation-item selected" role="menuitem" tabindex="0">
              <span class="select-menu-item-icon octicon octicon octicon-check"></span>
              <div class="select-menu-item-text">
                <input checked="checked" id="do_subscribed" name="do" type="radio" value="subscribed" />
                <h4>Watching</h4>
                <span class="description">You receive notifications for all conversations in this repository.</span>
                <span class="js-select-button-text hidden-select-button-text">
                  <span class="octicon octicon-eye-unwatch"></span>
                  Unwatch
                </span>
              </div>
            </div> <!-- /.select-menu-item -->

            <div class="select-menu-item js-navigation-item " role="menuitem" tabindex="0">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <div class="select-menu-item-text">
                <input id="do_ignore" name="do" type="radio" value="ignore" />
                <h4>Ignoring</h4>
                <span class="description">You do not receive any notifications for conversations in this repository.</span>
                <span class="js-select-button-text hidden-select-button-text">
                  <span class="octicon octicon-mute"></span>
                  Stop ignoring
                </span>
              </div>
            </div> <!-- /.select-menu-item -->

          </div> <!-- /.select-menu-list -->

        </div> <!-- /.select-menu-modal -->
      </div> <!-- /.select-menu-modal-holder -->
    </div> <!-- /.select-menu -->

</form>
    </li>

  <li>
  

  <div class="js-toggler-container js-social-container starring-container on">
    <a href="/astrolitterbox/growth-curve-photometry/unstar"
      class="minibutton with-count js-toggler-target star-button starred upwards"
      title="Unstar this repository" data-remote="true" data-method="post" rel="nofollow">
      <span class="octicon octicon-star-delete"></span><span class="text">Unstar</span>
    </a>

    <a href="/astrolitterbox/growth-curve-photometry/star"
      class="minibutton with-count js-toggler-target star-button unstarred upwards"
      title="Star this repository" data-remote="true" data-method="post" rel="nofollow">
      <span class="octicon octicon-star"></span><span class="text">Star</span>
    </a>

      <a class="social-count js-social-count" href="/astrolitterbox/growth-curve-photometry/stargazers">
        2
      </a>
  </div>

  </li>


        <li>
          <a href="/astrolitterbox/growth-curve-photometry/fork" class="minibutton with-count js-toggler-target fork-button lighter upwards" title="Fork this repo" rel="nofollow" data-method="post">
            <span class="octicon octicon-git-branch-create"></span><span class="text">Fork</span>
          </a>
          <a href="/astrolitterbox/growth-curve-photometry/network" class="social-count">0</a>
        </li>


</ul>

        <h1 itemscope itemtype="http://data-vocabulary.org/Breadcrumb" class="entry-title public">
          <span class="repo-label"><span>public</span></span>
          <span class="mega-octicon octicon-repo"></span>
          <span class="author">
            <a href="/astrolitterbox" class="url fn" itemprop="url" rel="author"><span itemprop="title">astrolitterbox</span></a>
          </span>
          <span class="repohead-name-divider">/</span>
          <strong><a href="/astrolitterbox/growth-curve-photometry" class="js-current-repository js-repo-home-link">growth-curve-photometry</a></strong>

          <span class="page-context-loader">
            <img alt="Octocat-spinner-32" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
          </span>

        </h1>
      </div><!-- /.container -->
    </div><!-- /.repohead -->

    

    <div class="container">

      <div class="repository-with-sidebar repo-container  ">

        <div class="repository-sidebar">
            

<div class="sunken-menu vertical-right repo-nav js-repo-nav js-repository-container-pjax js-octicon-loaders">
  <div class="sunken-menu-contents">
    <ul class="sunken-menu-group">
      <li class="tooltipped leftwards" title="Code">
        <a href="/astrolitterbox/growth-curve-photometry/tree/newProduction" aria-label="Code" class="selected js-selected-navigation-item sunken-menu-item" data-gotokey="c" data-pjax="true" data-selected-links="repo_source repo_downloads repo_commits repo_tags repo_branches /astrolitterbox/growth-curve-photometry/tree/newProduction">
          <span class="octicon octicon-code"></span> <span class="full-word">Code</span>
          <img alt="Octocat-spinner-32" class="mini-loader" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>

        <li class="tooltipped leftwards" title="Issues">
          <a href="/astrolitterbox/growth-curve-photometry/issues" aria-label="Issues" class="js-selected-navigation-item sunken-menu-item js-disable-pjax" data-gotokey="i" data-selected-links="repo_issues /astrolitterbox/growth-curve-photometry/issues">
            <span class="octicon octicon-issue-opened"></span> <span class="full-word">Issues</span>
            <span class='counter'>0</span>
            <img alt="Octocat-spinner-32" class="mini-loader" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
</a>        </li>

      <li class="tooltipped leftwards" title="Pull Requests"><a href="/astrolitterbox/growth-curve-photometry/pulls" aria-label="Pull Requests" class="js-selected-navigation-item sunken-menu-item js-disable-pjax" data-gotokey="p" data-selected-links="repo_pulls /astrolitterbox/growth-curve-photometry/pulls">
            <span class="octicon octicon-git-pull-request"></span> <span class="full-word">Pull Requests</span>
            <span class='counter'>0</span>
            <img alt="Octocat-spinner-32" class="mini-loader" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>


        <li class="tooltipped leftwards" title="Wiki">
          <a href="/astrolitterbox/growth-curve-photometry/wiki" aria-label="Wiki" class="js-selected-navigation-item sunken-menu-item" data-pjax="true" data-selected-links="repo_wiki /astrolitterbox/growth-curve-photometry/wiki">
            <span class="octicon octicon-book"></span> <span class="full-word">Wiki</span>
            <img alt="Octocat-spinner-32" class="mini-loader" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
</a>        </li>
    </ul>
    <div class="sunken-menu-separator"></div>
    <ul class="sunken-menu-group">

      <li class="tooltipped leftwards" title="Pulse">
        <a href="/astrolitterbox/growth-curve-photometry/pulse" aria-label="Pulse" class="js-selected-navigation-item sunken-menu-item" data-pjax="true" data-selected-links="pulse /astrolitterbox/growth-curve-photometry/pulse">
          <span class="octicon octicon-pulse"></span> <span class="full-word">Pulse</span>
          <img alt="Octocat-spinner-32" class="mini-loader" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>

      <li class="tooltipped leftwards" title="Graphs">
        <a href="/astrolitterbox/growth-curve-photometry/graphs" aria-label="Graphs" class="js-selected-navigation-item sunken-menu-item" data-pjax="true" data-selected-links="repo_graphs repo_contributors /astrolitterbox/growth-curve-photometry/graphs">
          <span class="octicon octicon-graph"></span> <span class="full-word">Graphs</span>
          <img alt="Octocat-spinner-32" class="mini-loader" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>

      <li class="tooltipped leftwards" title="Network">
        <a href="/astrolitterbox/growth-curve-photometry/network" aria-label="Network" class="js-selected-navigation-item sunken-menu-item js-disable-pjax" data-selected-links="repo_network /astrolitterbox/growth-curve-photometry/network">
          <span class="octicon octicon-git-branch"></span> <span class="full-word">Network</span>
          <img alt="Octocat-spinner-32" class="mini-loader" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>
    </ul>


      <div class="sunken-menu-separator"></div>
      <ul class="sunken-menu-group">
        <li class="tooltipped leftwards" title="Settings">
          <a href="/astrolitterbox/growth-curve-photometry/settings"
            class="sunken-menu-item" data-pjax aria-label="Settings">
            <span class="octicon octicon-tools"></span> <span class="full-word">Settings</span>
            <img alt="Octocat-spinner-32" class="mini-loader" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
          </a>
        </li>
      </ul>
  </div>
</div>

            <div class="only-with-full-nav">
              

  

<div class="clone-url open"
  data-protocol-type="http"
  data-url="/users/set_protocol?protocol_selector=http&amp;protocol_type=push">
  <h3><strong>HTTPS</strong> clone URL</h3>
  <div class="clone-url-box">
    <input type="text" class="clone js-url-field"
           value="https://github.com/astrolitterbox/growth-curve-photometry.git" readonly="readonly">

    <span class="js-zeroclipboard url-box-clippy minibutton zeroclipboard-button" data-clipboard-text="https://github.com/astrolitterbox/growth-curve-photometry.git" data-copied-hint="copied!" title="copy to clipboard"><span class="octicon octicon-clippy"></span></span>
  </div>
</div>

  

<div class="clone-url "
  data-protocol-type="ssh"
  data-url="/users/set_protocol?protocol_selector=ssh&amp;protocol_type=push">
  <h3><strong>SSH</strong> clone URL</h3>
  <div class="clone-url-box">
    <input type="text" class="clone js-url-field"
           value="git@github.com:astrolitterbox/growth-curve-photometry.git" readonly="readonly">

    <span class="js-zeroclipboard url-box-clippy minibutton zeroclipboard-button" data-clipboard-text="git@github.com:astrolitterbox/growth-curve-photometry.git" data-copied-hint="copied!" title="copy to clipboard"><span class="octicon octicon-clippy"></span></span>
  </div>
</div>

  

<div class="clone-url "
  data-protocol-type="subversion"
  data-url="/users/set_protocol?protocol_selector=subversion&amp;protocol_type=push">
  <h3><strong>Subversion</strong> checkout URL</h3>
  <div class="clone-url-box">
    <input type="text" class="clone js-url-field"
           value="https://github.com/astrolitterbox/growth-curve-photometry" readonly="readonly">

    <span class="js-zeroclipboard url-box-clippy minibutton zeroclipboard-button" data-clipboard-text="https://github.com/astrolitterbox/growth-curve-photometry" data-copied-hint="copied!" title="copy to clipboard"><span class="octicon octicon-clippy"></span></span>
  </div>
</div>


<p class="clone-options">You can clone with
      <a href="#" class="js-clone-selector" data-protocol="http">HTTPS</a>,
      <a href="#" class="js-clone-selector" data-protocol="ssh">SSH</a>,
      or <a href="#" class="js-clone-selector" data-protocol="subversion">Subversion</a>.
  <span class="octicon help tooltipped upwards" title="Get help on which URL is right for you.">
    <a href="https://help.github.com/articles/which-remote-url-should-i-use">
    <span class="octicon octicon-question"></span>
    </a>
  </span>
</p>



              <a href="/astrolitterbox/growth-curve-photometry/archive/newProduction.zip"
                 class="minibutton sidebar-button"
                 title="Download this repository as a zip file"
                 rel="nofollow">
                <span class="octicon octicon-cloud-download"></span>
                Download ZIP
              </a>
            </div>
        </div><!-- /.repository-sidebar -->

        <div id="js-repo-pjax-container" class="repository-content context-loader-container" data-pjax-container>
          


<!-- blob contrib key: blob_contributors:v21:ad8d0b66411de1027a4eda0e199597ee -->

<p title="This is a placeholder element" class="js-history-link-replace hidden"></p>

<a href="/astrolitterbox/growth-curve-photometry/find/newProduction" data-pjax data-hotkey="t" class="js-show-file-finder" style="display:none">Show File Finder</a>

<div class="file-navigation">
  

<div class="select-menu js-menu-container js-select-menu" >
  <span class="minibutton select-menu-button js-menu-target" data-hotkey="w"
    data-master-branch="master"
    data-ref="newProduction"
    role="button" aria-label="Switch branches or tags" tabindex="0">
    <span class="octicon octicon-git-branch"></span>
    <i>branch:</i>
    <span class="js-select-button">newProduction</span>
  </span>

  <div class="select-menu-modal-holder js-menu-content js-navigation-container" data-pjax>

    <div class="select-menu-modal">
      <div class="select-menu-header">
        <span class="select-menu-title">Switch branches/tags</span>
        <span class="octicon octicon-remove-close js-menu-close"></span>
      </div> <!-- /.select-menu-header -->

      <div class="select-menu-filters">
        <div class="select-menu-text-filter">
          <input type="text" aria-label="Find or create a branch…" id="context-commitish-filter-field" class="js-filterable-field js-navigation-enable" placeholder="Find or create a branch…">
        </div>
        <div class="select-menu-tabs">
          <ul>
            <li class="select-menu-tab">
              <a href="#" data-tab-filter="branches" class="js-select-menu-tab">Branches</a>
            </li>
            <li class="select-menu-tab">
              <a href="#" data-tab-filter="tags" class="js-select-menu-tab">Tags</a>
            </li>
          </ul>
        </div><!-- /.select-menu-tabs -->
      </div><!-- /.select-menu-filters -->

      <div class="select-menu-list select-menu-tab-bucket js-select-menu-tab-bucket" data-tab-filter="branches">

        <div data-filterable-for="context-commitish-filter-field" data-filterable-type="substring">


            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/astrolitterbox/growth-curve-photometry/blob/master/vimos/sdss/readGalfit.py"
                 data-name="master"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text js-select-button-text css-truncate-target"
                 title="master">master</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item selected">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/astrolitterbox/growth-curve-photometry/blob/newProduction/vimos/sdss/readGalfit.py"
                 data-name="newProduction"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text js-select-button-text css-truncate-target"
                 title="newProduction">newProduction</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/astrolitterbox/growth-curve-photometry/blob/noSciPy/vimos/sdss/readGalfit.py"
                 data-name="noSciPy"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text js-select-button-text css-truncate-target"
                 title="noSciPy">noSciPy</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/astrolitterbox/growth-curve-photometry/blob/test/vimos/sdss/readGalfit.py"
                 data-name="test"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text js-select-button-text css-truncate-target"
                 title="test">test</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/astrolitterbox/growth-curve-photometry/blob/work/vimos/sdss/readGalfit.py"
                 data-name="work"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text js-select-button-text css-truncate-target"
                 title="work">work</a>
            </div> <!-- /.select-menu-item -->
        </div>

          <form accept-charset="UTF-8" action="/astrolitterbox/growth-curve-photometry/branches" class="js-create-branch select-menu-item select-menu-new-item-form js-navigation-item js-new-item-form" method="post"><div style="margin:0;padding:0;display:inline"><input name="authenticity_token" type="hidden" value="zLxAz81l0NOJ0PF6q68TRcyEIcMRBkTFmoXgF8jguBE=" /></div>
            <span class="octicon octicon-git-branch-create select-menu-item-icon"></span>
            <div class="select-menu-item-text">
              <h4>Create branch: <span class="js-new-item-name"></span></h4>
              <span class="description">from ‘newProduction’</span>
            </div>
            <input type="hidden" name="name" id="name" class="js-new-item-value">
            <input type="hidden" name="branch" id="branch" value="newProduction" />
            <input type="hidden" name="path" id="branch" value="vimos/sdss/readGalfit.py" />
          </form> <!-- /.select-menu-item -->

      </div> <!-- /.select-menu-list -->

      <div class="select-menu-list select-menu-tab-bucket js-select-menu-tab-bucket" data-tab-filter="tags">
        <div data-filterable-for="context-commitish-filter-field" data-filterable-type="substring">


        </div>

        <div class="select-menu-no-results">Nothing to show</div>
      </div> <!-- /.select-menu-list -->

    </div> <!-- /.select-menu-modal -->
  </div> <!-- /.select-menu-modal-holder -->
</div> <!-- /.select-menu -->

  <div class="breadcrumb">
    <span class='repo-root js-repo-root'><span itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="/astrolitterbox/growth-curve-photometry/tree/newProduction" data-branch="newProduction" data-direction="back" data-pjax="true" itemscope="url"><span itemprop="title">growth-curve-photometry</span></a></span></span><span class="separator"> / </span><span itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="/astrolitterbox/growth-curve-photometry/tree/newProduction/vimos" data-branch="newProduction" data-direction="back" data-pjax="true" itemscope="url"><span itemprop="title">vimos</span></a></span><span class="separator"> / </span><span itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="/astrolitterbox/growth-curve-photometry/tree/newProduction/vimos/sdss" data-branch="newProduction" data-direction="back" data-pjax="true" itemscope="url"><span itemprop="title">sdss</span></a></span><span class="separator"> / </span><strong class="final-path">readGalfit.py</strong> <span class="js-zeroclipboard minibutton zeroclipboard-button" data-clipboard-text="vimos/sdss/readGalfit.py" data-copied-hint="copied!" title="copy to clipboard"><span class="octicon octicon-clippy"></span></span>
  </div>
</div>


  <div class="commit commit-loader file-history-tease js-deferred-content" data-url="/astrolitterbox/growth-curve-photometry/contributors/newProduction/vimos/sdss/readGalfit.py">
    Fetching contributors…

    <div class="participation">
      <p class="loader-loading"><img alt="Octocat-spinner-32-eaf2f5" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32-EAF2F5.gif" width="16" /></p>
      <p class="loader-error">Cannot retrieve contributors at this time</p>
    </div>
  </div>

<div id="files" class="bubble">
  <div class="file">
    <div class="meta">
      <div class="info">
        <span class="icon"><b class="octicon octicon-file-text"></b></span>
        <span class="mode" title="File Mode">file</span>
          <span>43 lines (33 sloc)</span>
        <span>1.075 kb</span>
      </div>
      <div class="actions">
        <div class="button-group">
                <a class="minibutton"
                   href="/astrolitterbox/growth-curve-photometry/edit/newProduction/vimos/sdss/readGalfit.py"
                   data-method="post" rel="nofollow" data-hotkey="e">Edit</a>
          <a href="/astrolitterbox/growth-curve-photometry/raw/newProduction/vimos/sdss/readGalfit.py" class="button minibutton " id="raw-url">Raw</a>
            <a href="/astrolitterbox/growth-curve-photometry/blame/newProduction/vimos/sdss/readGalfit.py" class="button minibutton ">Blame</a>
          <a href="/astrolitterbox/growth-curve-photometry/commits/newProduction/vimos/sdss/readGalfit.py" class="button minibutton " rel="nofollow">History</a>
        </div><!-- /.button-group -->
          <a class="minibutton danger empty-icon tooltipped downwards"
             href="/astrolitterbox/growth-curve-photometry/delete/newProduction/vimos/sdss/readGalfit.py"
             title=""
             data-method="post" data-test-id="delete-blob-file" rel="nofollow">
          Delete
        </a>
      </div><!-- /.actions -->

    </div>
        <div class="blob-wrapper data type-python js-blob-data">
        <table class="file-code file-diff">
          <tr class="file-code-line">
            <td class="blob-line-nums">
              <span id="L1" rel="#L1">1</span>
<span id="L2" rel="#L2">2</span>
<span id="L3" rel="#L3">3</span>
<span id="L4" rel="#L4">4</span>
<span id="L5" rel="#L5">5</span>
<span id="L6" rel="#L6">6</span>
<span id="L7" rel="#L7">7</span>
<span id="L8" rel="#L8">8</span>
<span id="L9" rel="#L9">9</span>
<span id="L10" rel="#L10">10</span>
<span id="L11" rel="#L11">11</span>
<span id="L12" rel="#L12">12</span>
<span id="L13" rel="#L13">13</span>
<span id="L14" rel="#L14">14</span>
<span id="L15" rel="#L15">15</span>
<span id="L16" rel="#L16">16</span>
<span id="L17" rel="#L17">17</span>
<span id="L18" rel="#L18">18</span>
<span id="L19" rel="#L19">19</span>
<span id="L20" rel="#L20">20</span>
<span id="L21" rel="#L21">21</span>
<span id="L22" rel="#L22">22</span>
<span id="L23" rel="#L23">23</span>
<span id="L24" rel="#L24">24</span>
<span id="L25" rel="#L25">25</span>
<span id="L26" rel="#L26">26</span>
<span id="L27" rel="#L27">27</span>
<span id="L28" rel="#L28">28</span>
<span id="L29" rel="#L29">29</span>
<span id="L30" rel="#L30">30</span>
<span id="L31" rel="#L31">31</span>
<span id="L32" rel="#L32">32</span>
<span id="L33" rel="#L33">33</span>
<span id="L34" rel="#L34">34</span>
<span id="L35" rel="#L35">35</span>
<span id="L36" rel="#L36">36</span>
<span id="L37" rel="#L37">37</span>
<span id="L38" rel="#L38">38</span>
<span id="L39" rel="#L39">39</span>
<span id="L40" rel="#L40">40</span>
<span id="L41" rel="#L41">41</span>
<span id="L42" rel="#L42">42</span>

            </td>
            <td class="blob-line-code">
                    <div class="highlight"><pre><div class='line' id='LC1'><span class="kn">import</span> <span class="nn">pyfits</span></div><div class='line' id='LC2'><span class="kn">import</span> <span class="nn">numpy</span> <span class="kn">as</span> <span class="nn">np</span></div><div class='line' id='LC3'><span class="n">band</span> <span class="o">=</span> <span class="s">&#39;r&#39;</span></div><div class='line' id='LC4'><br/></div><div class='line' id='LC5'><br/></div><div class='line' id='LC6'><span class="k">def</span> <span class="nf">read_pa_ba_values</span><span class="p">(</span><span class="n">fileName</span><span class="p">,</span> <span class="n">galaxy</span><span class="p">):</span></div><div class='line' id='LC7'>&nbsp;&nbsp;<span class="n">hdulist</span> <span class="o">=</span> <span class="n">pyfits</span><span class="o">.</span><span class="n">open</span><span class="p">(</span><span class="n">fileName</span><span class="p">)</span></div><div class='line' id='LC8'>&nbsp;&nbsp;<span class="n">tbdata</span> <span class="o">=</span> <span class="n">hdulist</span><span class="p">[</span><span class="mi">1</span><span class="p">]</span><span class="o">.</span><span class="n">data</span> </div><div class='line' id='LC9'>&nbsp;&nbsp;<span class="k">print</span> <span class="n">galaxy</span><span class="p">,</span> <span class="n">fileName</span><span class="p">,</span> <span class="n">tbdata</span><span class="o">.</span><span class="n">field</span><span class="p">(</span><span class="s">&#39;Name&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">shape</span></div><div class='line' id='LC10'>&nbsp;&nbsp;<span class="k">if</span> <span class="n">galaxy</span> <span class="ow">in</span> <span class="n">tbdata</span><span class="o">.</span><span class="n">field</span><span class="p">(</span><span class="s">&#39;Name&#39;</span><span class="p">):</span></div><div class='line' id='LC11'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">ind</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">where</span><span class="p">(</span><span class="n">tbdata</span><span class="o">.</span><span class="n">field</span><span class="p">(</span><span class="s">&#39;Name&#39;</span><span class="p">)</span> <span class="o">==</span> <span class="n">galaxy</span><span class="p">)</span></div><div class='line' id='LC12'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">ba</span> <span class="o">=</span> <span class="n">tbdata</span><span class="o">.</span><span class="n">field</span><span class="p">(</span><span class="s">&#39;disc_ba&#39;</span><span class="p">)[</span><span class="n">ind</span><span class="p">]</span></div><div class='line' id='LC13'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">pa</span> <span class="o">=</span> <span class="n">tbdata</span><span class="o">.</span><span class="n">field</span><span class="p">(</span><span class="s">&#39;disc_PA&#39;</span><span class="p">)[</span><span class="n">ind</span><span class="p">]</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  </div><div class='line' id='LC14'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="n">ba</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span> <span class="n">pa</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span></div><div class='line' id='LC15'>&nbsp;&nbsp;<span class="k">else</span><span class="p">:</span></div><div class='line' id='LC16'>&nbsp;&nbsp;&nbsp;<span class="k">raise</span> <span class="ne">Exception</span><span class="p">(</span><span class="s">&#39;NotInFile&#39;</span><span class="p">)</span></div><div class='line' id='LC17'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div><div class='line' id='LC18'><br/></div><div class='line' id='LC19'><span class="n">barFile</span> <span class="o">=</span> <span class="s">&#39;GALFIT_discbarbulge.&#39;</span><span class="o">+</span><span class="n">band</span><span class="o">+</span><span class="s">&#39;.fits&#39;</span></div><div class='line' id='LC20'><span class="n">bulgeFile</span> <span class="o">=</span> <span class="s">&#39;GALFIT_discbulge.&#39;</span><span class="o">+</span><span class="n">band</span><span class="o">+</span><span class="s">&#39;.fits&#39;</span></div><div class='line' id='LC21'><span class="n">discFile</span> <span class="o">=</span> <span class="s">&#39;GALFIT_disc.&#39;</span><span class="o">+</span><span class="n">band</span><span class="o">+</span><span class="s">&#39;.fits&#39;</span></div><div class='line' id='LC22'><br/></div><div class='line' id='LC23'><span class="n">val</span> <span class="o">=</span> <span class="p">[]</span></div><div class='line' id='LC24'><br/></div><div class='line' id='LC25'><span class="n">galaxyList</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">genfromtxt</span><span class="p">(</span><span class="s">&#39;list.csv&#39;</span><span class="p">,</span> <span class="n">dtype</span><span class="o">=</span><span class="s">&#39;object&#39;</span><span class="p">)</span></div><div class='line' id='LC26'><br/></div><div class='line' id='LC27'><br/></div><div class='line' id='LC28'><span class="k">for</span> <span class="n">galaxy</span> <span class="ow">in</span> <span class="n">galaxyList</span><span class="p">:</span></div><div class='line' id='LC29'>&nbsp;&nbsp;<span class="k">try</span><span class="p">:</span></div><div class='line' id='LC30'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">ba</span><span class="p">,</span> <span class="n">pa</span> <span class="o">=</span> <span class="n">read_pa_ba_values</span><span class="p">(</span><span class="n">barFile</span><span class="p">,</span> <span class="n">galaxy</span><span class="p">)</span></div><div class='line' id='LC31'>&nbsp;&nbsp;<span class="k">except</span> <span class="ne">Exception</span><span class="p">:</span></div><div class='line' id='LC32'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="c">#print &#39;no bar&#39;</span></div><div class='line' id='LC33'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">try</span><span class="p">:</span></div><div class='line' id='LC34'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">ba</span><span class="p">,</span> <span class="n">pa</span> <span class="o">=</span> <span class="n">read_pa_ba_values</span><span class="p">(</span><span class="n">bulgeFile</span><span class="p">,</span> <span class="n">galaxy</span><span class="p">)</span></div><div class='line' id='LC35'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">except</span> <span class="ne">Exception</span><span class="p">:</span></div><div class='line' id='LC36'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="c">#print &#39;no bulge&#39;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></div><div class='line' id='LC37'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">ba</span><span class="p">,</span> <span class="n">pa</span> <span class="o">=</span> <span class="n">read_pa_ba_values</span><span class="p">(</span><span class="n">discFile</span><span class="p">,</span> <span class="n">galaxy</span><span class="p">)</span></div><div class='line' id='LC38'>&nbsp;&nbsp;<span class="k">print</span> <span class="n">ba</span><span class="p">,</span> <span class="n">pa</span>  </div><div class='line' id='LC39'>&nbsp;&nbsp;<span class="n">val</span><span class="o">.</span><span class="n">append</span><span class="p">([</span><span class="n">galaxy</span><span class="p">,</span> <span class="n">ba</span><span class="p">,</span> <span class="n">pa</span><span class="p">])</span></div><div class='line' id='LC40'><span class="n">val</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">asarray</span><span class="p">(</span><span class="n">val</span><span class="p">,</span> <span class="n">dtype</span><span class="o">=</span><span class="s">&#39;object&#39;</span><span class="p">)</span></div><div class='line' id='LC41'><span class="n">np</span><span class="o">.</span><span class="n">savetxt</span><span class="p">(</span><span class="s">&#39;ba_pa_values.csv&#39;</span><span class="p">,</span> <span class="n">val</span><span class="p">,</span> <span class="n">delimiter</span><span class="o">=</span><span class="s">&#39;,&#39;</span><span class="p">,</span> <span class="n">fmt</span><span class="o">=</span><span class="s">&#39;</span><span class="si">%s</span><span class="s">, </span><span class="si">%f</span><span class="s">, </span><span class="si">%f</span><span class="s">&#39;</span><span class="p">)</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  </div><div class='line' id='LC42'><br/></div></pre></div>
            </td>
          </tr>
        </table>
  </div>

  </div>
</div>

<a href="#jump-to-line" rel="facebox[.linejump]" data-hotkey="l" class="js-jump-to-line" style="display:none">Jump to Line</a>
<div id="jump-to-line" style="display:none">
  <form accept-charset="UTF-8" class="js-jump-to-line-form">
    <input class="linejump-input js-jump-to-line-field" type="text" placeholder="Jump to line&hellip;" autofocus>
    <button type="submit" class="button">Go</button>
  </form>
</div>

        </div>

      </div><!-- /.repo-container -->
      <div class="modal-backdrop"></div>
    </div><!-- /.container -->
  </div><!-- /.site -->


    </div><!-- /.wrapper -->

      <div class="container">
  <div class="site-footer">
    <ul class="site-footer-links right">
      <li><a href="https://status.github.com/">Status</a></li>
      <li><a href="http://developer.github.com">API</a></li>
      <li><a href="http://training.github.com">Training</a></li>
      <li><a href="http://shop.github.com">Shop</a></li>
      <li><a href="/blog">Blog</a></li>
      <li><a href="/about">About</a></li>

    </ul>

    <a href="/">
      <span class="mega-octicon octicon-mark-github"></span>
    </a>

    <ul class="site-footer-links">
      <li>&copy; 2013 <span title="0.07793s from github-fe128-cp1-prd.iad.github.net">GitHub</span>, Inc.</li>
        <li><a href="/site/terms">Terms</a></li>
        <li><a href="/site/privacy">Privacy</a></li>
        <li><a href="/security">Security</a></li>
        <li><a href="/contact">Contact</a></li>
    </ul>
  </div><!-- /.site-footer -->
</div><!-- /.container -->


    <div class="fullscreen-overlay js-fullscreen-overlay" id="fullscreen_overlay">
  <div class="fullscreen-container js-fullscreen-container">
    <div class="textarea-wrap">
      <textarea name="fullscreen-contents" id="fullscreen-contents" class="js-fullscreen-contents" placeholder="" data-suggester="fullscreen_suggester"></textarea>
          <div class="suggester-container">
              <div class="suggester fullscreen-suggester js-navigation-container" id="fullscreen_suggester"
                 data-url="/astrolitterbox/growth-curve-photometry/suggestions/commit">
              </div>
          </div>
    </div>
  </div>
  <div class="fullscreen-sidebar">
    <a href="#" class="exit-fullscreen js-exit-fullscreen tooltipped leftwards" title="Exit Zen Mode">
      <span class="mega-octicon octicon-screen-normal"></span>
    </a>
    <a href="#" class="theme-switcher js-theme-switcher tooltipped leftwards"
      title="Switch themes">
      <span class="octicon octicon-color-mode"></span>
    </a>
  </div>
</div>



    <div id="ajax-error-message" class="flash flash-error">
      <span class="octicon octicon-alert"></span>
      <a href="#" class="octicon octicon-remove-close close ajax-error-dismiss"></a>
      Something went wrong with that request. Please try again.
    </div>

  </body>
</html>

