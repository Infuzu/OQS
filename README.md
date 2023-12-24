# `OQS` (Open Quick Script)
## Overview
`OQS` or `Open Quick Script` is an expression language intended to be universally adoptable, streamlined, and system-neutral scripting language that integrates effortlessly into diverse platforms. 

`OQS` is not designed to be a feature complete programming language. Rather, it is designed to be a simple, yet powerful, expression engine. It is specifically crafted to process expressions encompassing fundamental types and operations, interpreting a solitary expression—optionally accompanied by a dictionary, map, or JSON containing variables—to yield a consistent and logical outcome.




## Specification
The [language specification](https://github.com/Infuzu/OQS/blob/main/oqs-specification.md) was writen as a guide for anyone seeking to write an implementation of `OQS`. It is a living document and will be updated on regular intervals to keep up with the languages developing needs. 



## Versioning
There is a full change history of everything in this repository available in this repository by going through the git changes.

The [language specification](https://github.com/Infuzu/OQS/blob/main/oqs-specification.md) contains the current version of the language. There is also a folder in this repository called ['specification_history'](https://github.com/Infuzu/OQS/tree/main/specification_history) that contains a copy of all versions of the [specification](https://github.com/Infuzu/OQS/blob/main/oqs-specification.md).

All sample implementations should also contain their version history. Details about this should be in the sample implementation README.md.




## Sample Implementations
In order to ensure the accessibility of `OQS`, our team puts a lot of effort into maintaining a few implementations of `OQS` for public use. 

**Note**: These implementations are not built to be very feature rich. They are simply built to demonstrate the simplicity of `OQS` and ensure that there are open-source and free versions of language available for the public to use and build from if they so chose.

The current implementations maintained by the `OQS` team are as follows:
- [**Python**](https://github.com/Infuzu/OQS/tree/main/python_oqs_implementation). The full code of the implementation is available in the folder named ['python_oqs_implementation'](https://github.com/Infuzu/OQS/tree/main/python_oqs_implementation) at the base of this repository. If you with to use this implementation, you can follow the instructions listed in the [README for python implementation](https://github.com/Infuzu/OQS/blob/main/python_oqs_implementation/README.md).




## Custom Implementation
The `OQS` language is designed to be open and universal. We encourage everyone to build their own implementations of this language for private or public use. The [specification guide](https://github.com/Infuzu/OQS/blob/main/oqs-specification.md) is there to assist with that. Therefor, we ask that all implementations abide by the same [specification](https://github.com/Infuzu/OQS/blob/main/oqs-specification.md) and are built in such a way that anyone writing an expression for one implementation would be able to use the same expression across any implementation and expect the same results. There is a file in the root of this directory named [tests.json](https://github.com/Infuzu/OQS/blob/main/tests.json) in order to assist with that. We ask that all implementations be built in such a way that it can pass all tests specified there.




## License
`OQS` is dedicated to remaining an open-source project accessible to all. We have chosen the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) for `OQS`. This license permits free use, modification, distribution, and even commercial exploitation, provided that appropriate credit is given to the original creators.

We endorse the principles of open-source and encourage the community to engage with, enhance, and disseminate `OQS` while respecting the terms of this license.

For complete license details, refer to the [LICENSE](https://github.com/Infuzu/OQS/blob/main/LICENSE) file in the repository.




## How to Contribute
Contributions to `OQS` are warmly welcomed and greatly appreciated. Here are ways you can contribute:

- **Submitting Bug Reports or Feature Requests**: Use the [Issues](https://github.com/Infuzu/OQS/issues) section to report bugs or suggest new features.
- **Improving Documentation**: Enhance the existing documentation or write tutorials.
- **Submitting Pull Requests**: Fork the repository, create a new branch for your work, and submit a pull request.




## Authors and Contributors
The `OQS` language and the language specification are supported and maintained by [Infuzu](https://infuzu.com).

[Yidi Sprei](https://yidisprei.com) is the founding author of `OQS` and wrote the first version of the [specification](https://github.com/Infuzu/OQS/blob/main/oqs-specification.md).

The following individuals are core maintainers of the [Python OQS Implementation](https://github.com/Infuzu/OQS/tree/main/python_oqs_implementation):
- [Yidi Sprei](https://yidisprei.com)
