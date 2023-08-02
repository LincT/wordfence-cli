import regex

from ..intel.signatures import CommonString, Signature, SignatureSet

regex.DEFAULT_VERSION = regex.VERSION1


class MatchResult:

    def __init__(self, matches: list):
        self.matches = matches

    def matches(self) -> bool:
        return len(self.matches) > 0


class Matcher:

    def __init__(self, signature_set: SignatureSet):
        self.signature_set = signature_set


class MatcherContext:
    pass


class RegexMatcherContext(MatcherContext):

    def __init__(self, matcher):
        self.matcher = matcher
        self.signatures_without_common_strings = \
            self._extract_signatures_without_common_strings(matcher)
        self.common_string_states = self._initialize_common_string_states()
        self.matches = {}

    def _extract_signatures_without_common_strings(
                self,
                matcher: Matcher
            ) -> list:
        signatures = []
        for identifier, signature in matcher.signatures.items():
            if not signature.signature.has_common_strings():
                signatures.append(signature)
        return signatures

    def _initialize_common_string_states(self) -> list:
        states = []
        for common_string in self.matcher.common_strings:
            states.append(False)
        return states

    def _check_common_strings(self, chunk: bytes) -> list:
        common_string_counts = {}
        for index, common_string in enumerate(self.matcher.common_strings):
            if not self.common_string_states[index]:
                match = common_string.pattern.search(chunk)
                if match is not None:
                    self.common_string_states[index] = True
            if self.common_string_states[index]:
                sig_count = len(common_string.common_string.signature_ids)
                for identifier in common_string.common_string.signature_ids:
                    if identifier in self.matches:
                        continue
                    if identifier in common_string_counts:
                        common_string_counts[identifier] += 1
                    else:
                        common_string_counts[identifier] = 1
        possible_signatures = []
        for identifier, count in common_string_counts.items():
            signature = self.matcher.signatures[identifier]
            if count == signature.signature.get_common_string_count():
                possible_signatures.append(signature)
        return possible_signatures

    def _match_signature(self, signature: Signature, chunk: str):
        if not signature.is_valid():
            return
        match = signature.get_pattern().search(chunk)
        if match is not None:
            self.matches[signature.signature.identifier] = True

    def process_chunk(self, chunk: bytes) -> None:
        chunk = chunk.decode('utf-8', 'ignore')
        possible_signatures = self._check_common_strings(chunk)
        for signature in self.signatures_without_common_strings:
            self._match_signature(signature, chunk)
        for signature in possible_signatures:
            self._match_signature(signature, chunk)

    def get_matches(self) -> list:
        return self.matches


class RegexCommonString:

    def __init__(self, common_string: CommonString):
        self.common_string = common_string
        self.pattern = regex.compile(common_string.string)


class RegexSignature:

    def __init__(self, signature: Signature):
        self.signature = signature
        if not signature.has_common_strings():
            self.compile()

    def is_valid(self) -> bool:
        return self.get_pattern() is not None

    def compile(self) -> None:
        try:
            rule = self.signature.rule
            self.pattern = regex.compile(rule)
        except BaseException as error:
            print('Regex compilation for signature ' +
                  str(self.signature.identifier) +
                  ' failed: ' +
                  str(error) +
                  ', pattern: ' +
                  repr(rule))
            self.pattern = None
            # raise error #TODO: How should this be handled

    def get_pattern(self) -> regex.Pattern:
        # Signature patterns are compiled lazily as they are only needed if
        # common strings are matched and compiling all takes several seconds
        if not hasattr(self, 'pattern'):
            self.compile()
        return self.pattern


class RegexMatcher(Matcher):

    def __init__(self, signature_set: SignatureSet):
        super().__init__(signature_set)
        self._compile_regexes()

    def _compile_common_strings(self) -> None:
        self.common_strings = [
                RegexCommonString(common_string)
                for common_string in self.signature_set.common_strings
            ]

    def _compile_signatures(self) -> None:
        self.signatures = {}
        for identifier, signature in self.signature_set.signatures.items():
            self.signatures[identifier] = RegexSignature(signature)

    def _compile_regexes(self) -> None:
        self._compile_common_strings()
        self._compile_signatures()

    def create_context(self) -> RegexMatcherContext:
        return RegexMatcherContext(self)