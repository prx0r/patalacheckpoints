AnyStyle.io

- 

AnyStyle

# Parses academic references in no time!
Copy &amp; paste your bibliography below to get started …

Star on GitHub

Install RubyGem

# Documentation

## Web Application

### 1. Parse

To get started, simply paste your list of citation references into the textarea above. AnyStyle processes one reference per line so please make sure each reference starts on a new line and remove any superfluous line breaks. Empty lines are fine, though, the parser will just skip them.

When you're ready, hit the parse button!
### 2. Edit

AnyStyle splits your references into segments (author, title etc.) based on machine learning heuristics. These segments will be displayed in the token editor above. Please review each segment to make sure the results are correct; in case the parser got something wrong just select individual tokens like you would select text in your favourite text editor and click on the Assign label button to assign the correct label to your selection.

Pro tip: use Shift and Ctrl/Command to make multiple selections or double-click to select an entire segment at once.

When using the token editor, note that the parser requires every token to be assigned a label and the individual segments to be contiguous. For the best results combine tokens which semantically belong together. The word in, for example, typically belongs to either the editor or container-title segments (in fact it is a good indicator for those fields). When in doubt how to label a reference, please get in touch with us or take a look at our core [training data](https://github.com/inukshuk/anystyle/blob/master/res/parser/core.xml) for examples of correctly labelled references.
### 3. Save

That's it! When you've reviewed the segments just click on one of the available output formats to convert and save your references.

But there is more: because AnyStyle is based on machine learning you can help us improve! If the parser produces poor results for your citation style or language, just use the token editor to correctly label a handful of references; when you save the results, we will extract your adjustments and use them to train the parser; give us a few minutes to crunch numbers and try to parse your references again using the updated model: we hope the results will be much improved!

Pro tip: the current model's timestamp is included at the bottom of the parsed results; when training the model, keep an eye on the time to see whether or not your training data was already merged into the model.

Please note that we receive a lot of training data; too much or inconsistently-labelled data can cause the model to deteriorate so we may reset the model from time to time. Please let us know if training the model does not work for you or if your parse results are poor so we can take a look. Also, if you'd be interested in helping us curate the training data, your help is much appreciated!

## RubyGem

AnyStyle is open source software and freely available as a RubyGem!

```
$ [sudo] gem install anystyle&#x000A;
```

After installing the Gem you can start parsing references on your own computer directly from Ruby like this:

```
>> require "anystyle"&#x000A;&#x000A;>> AnyStyle.parse """&#x000A;    Turing, Alan, Computing Machinery and Intelligence, Mind 59, pp 433-460 (1950)&#x000A;   """&#x000A;=> [{&#x000A;     :type => "article-journal",&#x000A;     :author => [{ :family => "Turing", :given => "Alan" }],&#x000A;     :date => ["1950"],&#x000A;     :title => ["Computing Machinery and Intelligence"],&#x000A;     :"container-title" => ["Mind"],&#x000A;     :volume => ["59"],&#x000A;     :pages => ["433–460"],&#x000A;     :language => "en",&#x000A;     :scripts => ["Common", "Latin"]&#x000A;   }]&#x000A;
```

The RubyGem also includes a finder module to extract references from ful-text PDF documents.
For more details on how to use and train the parser and finder, please consult the [API documentation](https://rubydoc.info/gems/anystyle).

## On the Command Line

AnyStyle also has a command-line interface.

```
$ [sudo] gem install anystyle-cli&#x000A;
```

After installing the Gem you can start parsing references on your own computer directly from Ruby like this:

```
$ anystyle --help&#x000A;&#x000A;NAME&#x000A;    anystyle - Finds and parses bibliographic references&#x000A;&#x000A;SYNOPSIS&#x000A;    anystyle [global options] command [command options] [arguments...]&#x000A;&#x000A;VERSION&#x000A;    1.3.3 (cli 1.2.0, data 1.2.0)&#x000A;&#x000A;GLOBAL OPTIONS&#x000A;    -F, --finder-model=file - Set the finder model file (default: none)&#x000A;    -P, --parser-model=file - Set the parser model file (default: none)&#x000A;    --adapter=name          - Set the dictionary adapter (default: ruby)&#x000A;    -f, --format=name       - Set the output format (default: ["json"])&#x000A;    --pdfinfo=path          - Set the path for pdfinfo (default: none)&#x000A;    --pdftotext=path        - Set the path for pdftotext (default: none)&#x000A;    --help                  - Show this message&#x000A;    --[no-]stdout           - Print results directly to stdout&#x000A;    --[no-]verbose          - Print status messages to stderr&#x000A;    --version               - Display the program version&#x000A;    -w, --[no-]overwrite    - Allow overwriting existing files&#x000A;&#x000A;COMMANDS&#x000A;    check   - Check tagged documents or references&#x000A;    find    - Find and extract references from text documents&#x000A;    help    - Shows a list of commands or help for one command&#x000A;    license - Print license information&#x000A;    parse   - Parse and convert references&#x000A;    train   - Create a new finder or parser model&#x000A;
```

# Want to know more?

AnyStyle.io is a free service and provided as is
 without warranty of any kind. It is intended for non-commercial,
 limited use only, and its performance and function time
 is not guaranteed in any way.

We believe that there are better ways to spend your time than to parse bibliographies by hand; and isn't it precisely at this sort of tedious work that machines are supposed to excel? We hope this one will! However, if you find a bug or have an idea for improvement that we missed, you're welcome to open an issue or feature request.

[Report an issue!](https://github.com/inukshuk/anystyle/issues)

AnyStyle uses powerful machine learning heuristics based on [Conditional Random Fields](https://en.wikipedia.org/wiki/Conditional_random_field) that can be trained by everyone using our built-in editor. If you would like to support us, require more advanced adjustments, a custom model or want to integrate a similar parser into your own site or product, we'll be happy to work with you.

[Get in touch!](mailto:sylvester@keil.or.at)

Developed by [Sylvester Keil](https://github.com/inukshuk).
Designed by [Flachware](http://flachware.com).
With  at aliceblue.

- v1.5.0
- [GitHub](https://github.com/inukshuk/anystyle)
- [Issues](https://github.com/inukshuk/anystyle/issues)
- [RubyDoc](https://rubydoc.info/gems/anystyle)
- [RubyGem](https://rubygems.org/gems/anystyle)