# DeathMetal

"We are here to make ~~coffee~~ APT metal. We will make everything metal. Blacker than the blackest black times infinity."

DeathMetal is a suite of tools that interact with Intel AMT. Its kind of a foray into a world filled with intrigue and reversing puzzles with useful results.

Since this is super serious, tools are named after Metalocalypse characters.

Tools are prefixed with "dm_" to help with tab-completion and recognition.
* dm_pickles - Duckyscript interpreter that communicates over AMT KVM (vnc) and injects keystrokes. 
* dm_toki    - IDE-R implementation - lets you attach floopy and CD images remotely to the target computer.
* dm_nathan  - Is a cli that allows for configuring AMT via authenticated channel
* dm_rockso  - Presence and version scanner, can help you find AMT capable systems regardless of provisioning status. (works even if explicitly not-enabled)

Code that is common to more than one tool lives in a library called 'Charles', at the moment it can pretty much just help set up Redirection service stuff.

## Getting Started

You may want to run in a virtual env and install any dependencies that come up - the code is in python3.

### Prerequisites

Python3 and pip

### Installing

PIP

```
First, I would make a virtual python3 environment and activate it.
pip install git+https://github.com/Coalfire-Research/DeathMetal.git
```

## Built With
* Python3 default libs
* hexdump for debugging
* requests for http.

## Contributing
Submit a pull request, or talk to me or something.

## Authors

* **Victor Teissler** - *Initial work* - [Victor Teissler](https://github.com/Victor-Teissler)

See also the list of [contributors](https://github.com/Coalfire-Research/DeathMetal/contributors) who participated in this project.

## License

This project is licensed under a modified MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* Jimmy Twotimes for pointing me at the scanning capabilities - this became rockso, thanks man!
* Clutchisback for the beef hooks and help with the blog post - greatly appreciated.
* Soen knows what he did.
* Coalfire for the opportunity
