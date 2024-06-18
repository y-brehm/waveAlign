from wavealign.caching.single_file_cache import SingleFileCache


def replace_existing_cache(
        original_cache_list: list[SingleFileCache], new_single_file_cache: SingleFileCache
        ) -> list[SingleFileCache]:
    if original_cache_list is None:
        return [new_single_file_cache]

    for i, original_single_file_cache in enumerate(original_cache_list):
        if original_single_file_cache.file_path == new_single_file_cache.file_path:
            original_cache_list[i] = new_single_file_cache
            break
    else:
        original_cache_list.append(new_single_file_cache)

    return original_cache_list
